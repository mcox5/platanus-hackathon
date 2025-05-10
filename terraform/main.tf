terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
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

module "security" {
  source = "./modules/security"
  
  app_name    = var.app_name
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
}

module "ecr" {
  source = "./modules/ecr"
  
  app_name    = var.app_name
  environment = var.environment
}

module "ecs" {
  source = "./modules/ecs"
  
  app_name                 = var.app_name
  environment              = var.environment
  vpc_id                   = module.vpc.vpc_id
  public_subnet_ids        = module.vpc.public_subnet_ids
  app_security_group_id    = module.security.app_security_group_id
  alb_security_group_id    = module.security.alb_security_group_id
  ecs_task_execution_role  = module.iam.ecs_task_execution_role
  ecs_task_role            = module.iam.ecs_task_role
  ecr_repository_url       = module.ecr.repository_url
  container_port           = var.container_port
  db_host                  = module.rds.db_endpoint
  db_name                  = var.db_name
  db_username              = var.db_username
  db_password              = var.db_password
}

module "iam" {
  source = "./modules/iam"
  
  app_name    = var.app_name
  environment = var.environment
}
