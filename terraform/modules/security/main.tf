# Security Groups Module

# Load Balancer Security Group
resource "aws_security_group" "alb" {
  name        = "${var.app_name}-alb-sg-${var.environment}"
  description = "Controls access to the ALB"
  vpc_id      = var.vpc_id

  # Allow HTTP from anywhere (for redirects to HTTPS)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP traffic"
  }

  # Allow HTTPS from anywhere
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS traffic"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name        = "${var.app_name}-alb-sg-${var.environment}"
    Environment = var.environment
  }
}

# EC2 Application Server Security Group
resource "aws_security_group" "app" {
  name        = "${var.app_name}-app-sg-${var.environment}"
  description = "Allow inbound traffic to the application server"
  vpc_id      = var.vpc_id
  
  # Allow SSH traffic for management (optional, can be restricted to your IP)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }
  
  # Allow HTTP traffic from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP traffic"
  }
  
  # Allow HTTPS traffic from anywhere
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS traffic"
  }
  
  # Additional ports for custom application needs
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "FastAPI default port"
  }
  
  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }
  
  tags = {
    Name        = "${var.app_name}-app-sg-${var.environment}"
    Environment = var.environment
  }
}

# Database Security Group
resource "aws_security_group" "db" {
  name        = "${var.app_name}-db-sg-${var.environment}"
  description = "Allow inbound traffic to the database"
  vpc_id      = var.vpc_id
  
  # Allow PostgreSQL traffic from the application security group
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
    description     = "PostgreSQL traffic from application server"
  }
  
  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }
  
  tags = {
    Name        = "${var.app_name}-db-sg-${var.environment}"
    Environment = var.environment
  }
}
