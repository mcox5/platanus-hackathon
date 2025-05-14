###########################
# Route 53 Module
###########################

# Create the hosted zone (if it doesn't exist yet)
resource "aws_route53_zone" "main" {
  name = var.root_domain_name
  comment = "Managed by Terraform for ${var.app_name}-${var.environment}"

  tags = {
    Name        = "${var.app_name}-zone-${var.environment}"
    Environment = var.environment
  }
}

# Create an A record for the API subdomain
resource "aws_route53_record" "api" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.api_domain_name
  type    = "A"
  ttl     = "300"
  records = [var.elastic_ip]
}
