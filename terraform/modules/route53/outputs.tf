output "api_domain_fqdn" {
  description = "The fully qualified domain name for the API subdomain"
  value       = aws_route53_record.api.fqdn
}

output "zone_id" {
  description = "The hosted zone ID"
  value       = aws_route53_zone.main.zone_id
}

output "name_servers" {
  description = "The name servers for the hosted zone (needed for domain configuration)"
  value       = aws_route53_zone.main.name_servers
}
