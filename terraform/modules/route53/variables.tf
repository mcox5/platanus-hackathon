variable "app_name" {
  description = "Name of the application"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
}

variable "root_domain_name" {
  description = "Root domain name (e.g. meayudai.com)"
  type        = string
}

variable "api_domain_name" {
  description = "Subdomain name for API (e.g. api.meayudai.com)"
  type        = string
}

variable "elastic_ip" {
  description = "Elastic IP address to point the subdomain to"
  type        = string
}
