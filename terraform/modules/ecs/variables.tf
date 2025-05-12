variable "app_name" {
  description = "Name of the application"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "IDs of the public subnets"
  type        = list(string)
}

variable "app_security_group_id" {
  description = "ID of the app security group"
  type        = string
}

variable "alb_security_group_id" {
  description = "ID of the ALB security group"
  type        = string
}

variable "ecs_task_execution_role" {
  description = "ARN of the ECS task execution role"
  type        = string
}

variable "ecs_task_role" {
  description = "ARN of the ECS task role"
  type        = string
}

variable "ecr_repository_url" {
  description = "URL of the ECR repository"
  type        = string
}

variable "container_port" {
  description = "Port that the container exposes"
  type        = number
  default     = 8080
}

variable "task_cpu" {
  description = "CPU units for the ECS task"
  type        = number
  default     = 256 # 0.25 vCPU
}

variable "task_memory" {
  description = "Memory for the ECS task"
  type        = number
  default     = 512 # 0.5 GB
}

variable "app_count" {
  description = "Number of application instances to run"
  type        = number
  default     = 2
}

variable "db_host" {
  description = "Database host"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "instance_type" {
  description = "EC2 instance type for ECS"
  type        = string
  default     = "t3.small"
}

variable "key_name" {
  description = "Name of the SSH key pair for EC2 instance access"
  type        = string
}

variable "ecs_instance_role" {
  description = "IAM role for the ECS EC2 instance"
  type        = string
}
