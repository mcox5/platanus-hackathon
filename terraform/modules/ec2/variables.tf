variable "app_name" {
  description = "Name of the application"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small"
}

variable "subnet_id" {
  description = "ID of the subnet to place the EC2 instance in"
  type        = string
}

variable "security_group_id" {
  description = "ID of the security group for the EC2 instance"
  type        = string
}

variable "key_name" {
  description = "Name of the SSH key pair for the EC2 instance"
  type        = string
}

variable "db_host" {
  description = "Hostname:port of the database"
  type        = string
}

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_username" {
  description = "Username for the database"
  type        = string
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
