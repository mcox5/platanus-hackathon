###########################
# EC2 Instance Module
###########################

# Get latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instance
resource "aws_instance" "app_instance" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]
  key_name               = var.key_name
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  
  root_block_device {
    volume_type = "gp3"
    volume_size = 30
    encrypted   = true
  }
  
  # User data script to install Docker, docker-compose, postgres client, and set up the environment
  user_data = <<-EOF
    #!/bin/bash
    set -e

    # Update system packages
    yum update -y
    
    # Install Docker
    amazon-linux-extras install docker -y
    systemctl start docker
    systemctl enable docker
    usermod -a -G docker ec2-user
    
    # Install docker-compose
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Install PostgreSQL client
    amazon-linux-extras install postgresql13 -y
    
    # Install additional utilities
    yum install -y jq git vim
    
    # Create app directory
    mkdir -p /home/ec2-user/app
    chown ec2-user:ec2-user /home/ec2-user/app
    
    # Create environment file with database connection details
    cat > /home/ec2-user/app/.env << ENVFILE
    ENVIRONMENT=production
    DATABASE_URL=postgresql+asyncpg://${var.db_username}:${var.db_password}@${var.db_host}/${var.db_name}
    PROD_DB_USER=${var.db_username}
    PROD_DB_PASSWORD=${var.db_password}
    PROD_DB_HOST=${element(split(":", var.db_host), 0)}
    PROD_DB_PORT=${element(split(":", var.db_host), 1)}
    PROD_DB_NAME=${var.db_name}
    DB_USERNAME=${var.db_username}
    DB_PASSWORD=${var.db_password}
    DB_HOST=${element(split(":", var.db_host), 0)}
    DB_PORT=${element(split(":", var.db_host), 1)}
    DB_NAME=${var.db_name}
    ENVFILE
    
    # Create a script to import database dumps
    cat > /home/ec2-user/import-db.sh << SCRIPTFILE
    #!/bin/bash
    if [ -z "\$1" ]; then
      echo "Usage: ./import-db.sh path/to/dump.sql"
      exit 1
    fi
    
    echo "Importing database dump \$1 into PostgreSQL database ${var.db_name}..."
    PGPASSWORD="${var.db_password}" psql -h ${element(split(":", var.db_host), 0)} -p ${element(split(":", var.db_host), 1)} -U ${var.db_username} -d ${var.db_name} -f "\$1"
    echo "Import completed!"
    SCRIPTFILE
    
    chmod +x /home/ec2-user/import-db.sh
    chown ec2-user:ec2-user /home/ec2-user/import-db.sh
    
    # Create a helpful README file
    cat > /home/ec2-user/README.md << READMEFILE
    # Application Server Setup
    
    This server is configured to run the FastAPI application with Docker.
    
    ## Database Connection
    
    The database connection information is stored in \`/home/ec2-user/app/.env\`.
    
    ## Importing Database Dumps
    
    To import a database dump, use the following command:
    
    \`\`\`
    ./import-db.sh /path/to/your/dump.sql
    \`\`\`
    
    ## Running the Application
    
    1. Clone your repository:
       \`\`\`
       git clone <your-repository-url> app
       \`\`\`
       
    2. Build and run with Docker:
       \`\`\`
       cd app
       docker-compose up -d
       \`\`\`
    READMEFILE
    
    chown ec2-user:ec2-user /home/ec2-user/README.md
    
    # Signal that setup is complete
    touch /home/ec2-user/setup_complete
  EOF
  
  tags = {
    Name        = "${var.app_name}-instance-${var.environment}"
    Environment = var.environment
  }
}

# IAM role for EC2
resource "aws_iam_role" "ec2_role" {
  name = "${var.app_name}-ec2-role-${var.environment}"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
  
  tags = {
    Name        = "${var.app_name}-ec2-role-${var.environment}"
    Environment = var.environment
  }
}

# IAM policy for EC2 to access ECR
resource "aws_iam_policy" "ecr_access" {
  name        = "${var.app_name}-ecr-access-${var.environment}"
  description = "Allow EC2 to pull images from ECR"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetAuthorizationToken"
      ]
      Resource = "*"
    }]
  })
}

# Attach ECR access policy to EC2 role
resource "aws_iam_role_policy_attachment" "ecr_access_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.ecr_access.arn
}

# Attach SSM policy to EC2 role for management
resource "aws_iam_role_policy_attachment" "ssm_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# IAM instance profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.app_name}-ec2-profile-${var.environment}"
  role = aws_iam_role.ec2_role.name
}

# Elastic IP for EC2 instance
resource "aws_eip" "app_eip" {
  domain = "vpc"
  
  tags = {
    Name        = "${var.app_name}-eip-${var.environment}"
    Environment = var.environment
  }
}

# Associate Elastic IP with EC2 instance
resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.app_instance.id
  allocation_id = aws_eip.app_eip.id
}
