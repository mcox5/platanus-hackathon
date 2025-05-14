output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_instance.id
}

output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.app_eip.public_ip
}

output "private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.app_instance.private_ip
}

output "ssh_connection_string" {
  description = "SSH connection string to connect to the EC2 instance"
  value       = "ssh -i your-key.pem ec2-user@${aws_eip.app_eip.public_ip}"
}

output "instance_role" {
  description = "IAM role name of the EC2 instance"
  value       = aws_iam_role.ec2_role.name
}

output "instance_elastic_ip" {
  description = "Elastic IP address assigned to the EC2 instance"
  value       = aws_eip.app_eip.public_ip
}
