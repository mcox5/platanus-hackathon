output "key_name" {
  description = "Name of the created key pair in AWS"
  value       = aws_key_pair.app_key_pair.key_name
}

output "private_key_path" {
  description = "Path to the private key file for SSH access"
  value       = local_file.private_key.filename
}

output "public_key" {
  description = "Public key content (OpenSSH format)"
  value       = tls_private_key.ssh_key.public_key_openssh
  sensitive   = true
}
