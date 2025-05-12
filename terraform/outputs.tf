output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

# Database outputs
output "db_endpoint" {
  description = "Endpoint of the PostgreSQL RDS database"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "db_name" {
  description = "Name of the database"
  value       = var.db_name
}

# EC2 Instance outputs
output "ec2_instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.ec2.public_ip
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = module.ec2.instance_id
}

# SSH access outputs
output "ssh_key_path" {
  description = "Path to the SSH private key file"
  value       = module.key_pair.private_key_path
}

output "ssh_connection_string" {
  description = "SSH connection string to connect to the EC2 instance"
  value       = "ssh -i ${module.key_pair.private_key_path} ec2-user@${module.ec2.public_ip}"
}

# Docker repository output
output "ecr_repository_url" {
  description = "URL of the ECR repository for storing Docker images"
  value       = module.ecr.repository_url
}

# Database import command
output "database_import_command" {
  description = "Command to import a local SQL dump into the RDS database"
  value       = "PGPASSWORD=\"${var.db_password}\" psql -h ${element(split(":", module.rds.db_endpoint), 0)} -p ${element(split(":", module.rds.db_endpoint), 1)} -U ${var.db_username} -d ${var.db_name} -f /path/to/your/dump.sql"
  sensitive   = true
}
