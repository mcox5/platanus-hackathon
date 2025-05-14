variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "platanus-app"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# Database variables
variable "db_name" {
  description = "Name of the database"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Username for the database"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "Instance class for the RDS database"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage for the RDS database in GB"
  type        = number
  default     = 20
}

# Application variables
variable "container_port" {
  description = "Port that the container exposes"
  type        = number
  default     = 8080
}

variable "app_count" {
  description = "Number of application instances to run"
  type        = number
  default     = 2
}

# EC2 configuration
variable "ec2_instance_type" {
  description = "EC2 instance type for the ECS host"
  type        = string
  default     = "t3.small"
}

# Domain configuration
variable "root_domain_name" {
  description = "Root domain name (e.g. meayudai.com)"
  type        = string
  default     = "meayudai.com"
}

variable "api_subdomain" {
  description = "Subdomain for the API"
  type        = string
  default     = "api"
}
