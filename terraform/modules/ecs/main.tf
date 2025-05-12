locals {
  container_name = "${var.app_name}-container-${var.environment}"
  log_group_name = "/ecs/${var.app_name}-${var.environment}"
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "app" {
  name              = local.log_group_name
  retention_in_days = 30
  
  tags = {
    Name        = "${var.app_name}-log-group-${var.environment}"
    Environment = var.environment
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-cluster-${var.environment}"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name        = "${var.app_name}-cluster-${var.environment}"
    Environment = var.environment
  }
}

# Get latest Amazon Linux 2 ECS-optimized AMI
data "aws_ami" "ecs_optimized" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-*-x86_64-ebs"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instance for ECS
resource "aws_instance" "ecs" {
  ami                    = data.aws_ami.ecs_optimized.id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_ids[0]
  vpc_security_group_ids = [var.app_security_group_id]
  key_name               = var.key_name
  iam_instance_profile   = aws_iam_instance_profile.ecs_instance.name
  
  user_data = <<-EOF
    #!/bin/bash
    echo "ECS_CLUSTER=${aws_ecs_cluster.main.name}" >> /etc/ecs/ecs.config
    echo "ECS_ENABLE_TASK_IAM_ROLE=true" >> /etc/ecs/ecs.config
    echo "ECS_ENABLE_TASK_IAM_ROLE_NETWORK_HOST=true" >> /etc/ecs/ecs.config
  EOF
  
  root_block_device {
    volume_type = "gp3"
    volume_size = 30
  }
  
  tags = {
    Name        = "${var.app_name}-instance-${var.environment}"
    Environment = var.environment
  }
}

# IAM Instance Profile for EC2
resource "aws_iam_instance_profile" "ecs_instance" {
  name = "${var.app_name}-instance-profile-${var.environment}"
  role = var.ecs_instance_role
}

# ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.app_name}-task-${var.environment}"
  execution_role_arn      = var.ecs_task_execution_role
  task_role_arn           = var.ecs_task_role
  network_mode            = "bridge"
  requires_compatibilities = ["EC2"]
  
  container_definitions = jsonencode([
    {
      name      = local.container_name
      image     = "${var.ecr_repository_url}:latest"
      essential = true
      
      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]
      
      environment = [
        # Environment type
        {
          name  = "ENVIRONMENT"
          value = "production"
        },
        # Primary database connection string
        {
          name  = "DATABASE_URL"
          value = "postgresql+asyncpg://${var.db_username}:${var.db_password}@${var.db_host}/${var.db_name}"
        },
        # Individual database connection parameters
        {
          name  = "PROD_DB_USER"
          value = var.db_username
        },
        {
          name  = "PROD_DB_PASSWORD"
          value = var.db_password
        },
        {
          name  = "PROD_DB_HOST"
          value = split(":", var.db_host)[0]
        },
        {
          name  = "PROD_DB_PORT"
          value = try(split(":", var.db_host)[1], "5432")
        },
        {
          name  = "PROD_DB_NAME"
          value = var.db_name
        },
        # Additional database parameters with standard naming
        {
          name  = "DB_USERNAME"
          value = var.db_username
        },
        {
          name  = "DB_PASSWORD"
          value = var.db_password
        },
        {
          name  = "DB_HOST"
          value = split(":", var.db_host)[0]
        },
        {
          name  = "DB_PORT"
          value = try(split(":", var.db_host)[1], "5432")
        },
        {
          name  = "DB_NAME"
          value = var.db_name
        },
        # App hostname environment variable not needed for EC2 deployment
        {
          name  = "APP_HOSTNAME"
          value = "localhost"
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
      
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:${var.container_port}/ || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])
  
  tags = {
    Name        = "${var.app_name}-task-${var.environment}"
    Environment = var.environment
  }
}

# ECS Service
resource "aws_ecs_service" "app" {
  name            = "${var.app_name}-service-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1  # Single instance
  launch_type     = "EC2"
  
  tags = {
    Name        = "${var.app_name}-service-${var.environment}"
    Environment = var.environment
  }
  
  # Direct EC2 placement
  ordered_placement_strategy {
    type  = "binpack"
    field = "cpu"
  }
}
