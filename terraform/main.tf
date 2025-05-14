terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
  
  # Using local backend for now
  # Comment out the S3 backend until permissions are properly configured
  # backend "s3" {
  #   bucket = "meayudai-terraform-state-bucket"
  #   key    = "meayudai/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "aws" {
  region = var.aws_region
  profile = "source"
}

# Include different resource modules
module "vpc" {
  source = "./modules/vpc"
  
  app_name    = var.app_name
  environment = var.environment
  cidr_block  = var.vpc_cidr
}

module "security" {
  source = "./modules/security"
  
  app_name    = var.app_name
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
}

# SSH Key Pair for EC2 access
module "key_pair" {
  source = "./modules/key_pair"
  
  app_name    = var.app_name
  environment = var.environment
}

# PostgreSQL RDS Database
module "rds" {
  source = "./modules/rds"
  
  app_name                  = var.app_name
  environment               = var.environment
  vpc_id                    = module.vpc.vpc_id
  private_subnet_ids        = module.vpc.private_subnet_ids
  db_name                   = var.db_name
  db_username               = var.db_username
  db_password               = var.db_password
  db_instance_class         = var.db_instance_class
  db_allocated_storage      = var.db_allocated_storage
  db_security_group_id      = module.security.db_security_group_id
}

# EC2 Instance
module "ec2" {
  source = "./modules/ec2"
  
  app_name           = var.app_name
  environment        = var.environment
  instance_type      = var.ec2_instance_type
  subnet_id          = module.vpc.public_subnet_ids[0]
  security_group_id  = module.security.app_security_group_id
  key_name           = module.key_pair.key_name
  aws_region         = var.aws_region
  
  # Database connection information
  db_host            = module.rds.db_endpoint
  db_name            = var.db_name
  db_username        = var.db_username
  db_password        = var.db_password
}

# Optional: ECR Repository for Docker images
module "ecr" {
  source = "./modules/ecr"
  
  app_name    = var.app_name
  environment = var.environment
}

# Route 53 configuration for the API subdomain
module "route53" {
  source = "./modules/route53"
  
  app_name        = var.app_name
  environment     = var.environment
  root_domain_name = var.root_domain_name
  api_domain_name = "${var.api_subdomain}.${var.root_domain_name}"
  elastic_ip     = module.ec2.instance_elastic_ip
}

# No more ECS or IAM modules needed - all IAM roles are created in the EC2 module
