###########################
# SSH Key Pair Module
###########################

# Generate a secure RSA key
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create AWS key pair using the generated public key
resource "aws_key_pair" "app_key_pair" {
  key_name   = "${var.app_name}-key-${var.environment}"
  public_key = tls_private_key.ssh_key.public_key_openssh
  
  tags = {
    Name        = "${var.app_name}-key-${var.environment}"
    Environment = var.environment
  }
}

# Create a directory for storing keys if it doesn't exist
resource "null_resource" "key_directory" {
  provisioner "local-exec" {
    command = "mkdir -p ${path.root}/keys"
  }
}

# Save private key to file
resource "local_file" "private_key" {
  depends_on      = [null_resource.key_directory]
  content         = tls_private_key.ssh_key.private_key_pem
  filename        = "${path.root}/keys/${var.app_name}-key-${var.environment}.pem"
  file_permission = "0600"
}

# Output a helpful message about key location and permissions
resource "null_resource" "key_info" {
  depends_on = [local_file.private_key]
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "==========================================="
      echo "SSH private key saved to: ${local_file.private_key.filename}"
      echo "Use this key to SSH into your EC2 instance:"
      echo "chmod 600 ${local_file.private_key.filename}"
      echo "ssh -i ${local_file.private_key.filename} ec2-user@<EC2_PUBLIC_IP>"
      echo "==========================================="
    EOT
  }
}
