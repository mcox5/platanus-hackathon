output "key_name" {
  description = "Name of the created key pair"
  value       = aws_key_pair.generated_key.key_name
}

output "private_key_path" {
  description = "Path to the private key file"
  value       = local_file.private_key.filename
}
