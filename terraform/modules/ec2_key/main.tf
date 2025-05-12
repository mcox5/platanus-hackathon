resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = "${var.app_name}-key-${var.environment}"
  public_key = tls_private_key.ssh.public_key_openssh

  tags = {
    Name        = "${var.app_name}-key-${var.environment}"
    Environment = var.environment
  }
}

resource "local_file" "private_key" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${path.root}/keys/${var.app_name}-key-${var.environment}.pem"
  file_permission = "0600"
}
