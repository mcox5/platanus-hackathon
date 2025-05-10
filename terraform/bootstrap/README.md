# Terraform State Bucket Bootstrap

This directory contains Terraform configuration to create the S3 bucket that will be used to store the Terraform state for the main infrastructure.

## Purpose

Before you can use an S3 bucket as a Terraform backend, the bucket must exist. This configuration creates that bucket with appropriate settings:

- Bucket name: `meayudai-terraform-state-bucket`
- Versioning: Enabled
- Server-side encryption: AES-256
- Public access: Blocked

## How to Use

Run the following commands from this directory:

```bash
terraform init
terraform apply
```

Once the S3 bucket is created, you can go back to the main Terraform configuration and initialize it with the S3 backend.
