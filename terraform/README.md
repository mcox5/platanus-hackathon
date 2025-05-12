# Terraform Infrastructure for Platanus App

This directory contains Terraform configuration to deploy the Platanus application on AWS using a simpler EC2 + RDS architecture instead of the previous ECS Fargate setup.

## Architecture

The Terraform configuration sets up the following AWS resources:

- VPC with public and private subnets across multiple availability zones
- EC2 instance with Docker and PostgreSQL client pre-installed
- RDS PostgreSQL database for persistent storage
- ECR repository for container images (optional)
- Security groups for network protection
- SSH key pair for secure access to the EC2 instance

## Prerequisites

1. AWS CLI installed and configured
2. Terraform installed (v1.0 or later)
3. SSH client for connecting to the EC2 instance

## How to Deploy

1. **Initialize Terraform:**
   ```bash
   cd terraform
   terraform init
   ```

2. **Create or modify terraform.tfvars file:**
   Create a file named `terraform.tfvars` with the following variables:
   ```hcl
   aws_region           = "us-east-1"
   app_name             = "platanus-app"
   environment          = "prod"
   vpc_cidr             = "10.0.0.0/16"
   db_name              = "appdb"
   db_username          = "postgres"
   db_password          = "your-secure-password"  # Use a strong password
   db_instance_class    = "db.t3.micro"
   db_allocated_storage = 20
   ec2_instance_type    = "t3.small"
   ```

3. **Deploy the infrastructure:**
   ```bash
   terraform apply
   ```

4. **Connect to the EC2 instance:**
   After deployment is complete, Terraform will output the SSH connection details. 
   ```bash
   # Make the private key file accessible only to you
   chmod 600 $(terraform output -raw ssh_key_path)
   
   # Connect to the EC2 instance
   ssh -i $(terraform output -raw ssh_key_path) ec2-user@$(terraform output -raw ec2_instance_public_ip)
   ```

## Importing Data into the Database

You have two options to import your database dump:

### Option 1: Import from the EC2 instance

1. **Copy your SQL dump to the EC2 instance:**
   ```bash
   scp -i $(terraform output -raw ssh_key_path) path/to/your/dump.sql ec2-user@$(terraform output -raw ec2_instance_public_ip):~/
   ```

2. **Connect to the EC2 instance and run the import script:**
   ```bash
   ssh -i $(terraform output -raw ssh_key_path) ec2-user@$(terraform output -raw ec2_instance_public_ip)
   ./import-db.sh dump.sql
   ```

### Option 2: Import directly from your local machine

```bash
# Get the database connection details
DB_ENDPOINT=$(terraform output -raw db_endpoint)
DB_NAME=$(terraform output -raw db_name)
DB_USER="postgres"  # Replace with your database username
DB_PASSWORD="your-password"  # Replace with your database password

# Run the psql command to import the dump
PGPASSWORD="$DB_PASSWORD" psql -h $DB_ENDPOINT -U $DB_USER -d $DB_NAME -f /path/to/your/dump.sql
```

## Running Your Application

1. **SSH into the EC2 instance:**
   ```bash
   ssh -i $(terraform output -raw ssh_key_path) ec2-user@$(terraform output -raw ec2_instance_public_ip)
   ```

2. **Clone your application repository:**
   ```bash
   git clone <your-repository-url> app
   cd app
   ```

3. **Run with Docker:**
   ```bash
   # If you have a docker-compose.yml file
   docker-compose up -d
   
   # Or run the container directly
   docker run -d -p 8000:8000 --env-file /home/ec2-user/app/.env <your-image>
   ```
   
   All necessary environment variables for database connection are already set up in `/home/ec2-user/app/.env`.

## Accessing Your Application

After deploying your application on the EC2 instance, you can access it using:

```
http://$(terraform output -raw ec2_instance_public_ip):8000
```

You may need to adjust the port number based on your application's configuration.

## Using the ECR Repository (Optional)

If you want to use the included ECR repository to store your Docker images:

```bash
# Get the ECR repository URL
ECR_REPO=$(terraform output -raw ecr_repository_url)

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO

# Build and tag your image
docker build -t $ECR_REPO:latest .
docker push $ECR_REPO:latest
```

## Cleanup

To destroy the infrastructure when no longer needed:

```bash
terraform destroy
```

## Modules Overview

The infrastructure is organized into the following modules:

- **VPC**: Network infrastructure with public and private subnets
- **EC2**: Application server with Docker and PostgreSQL client
- **RDS**: PostgreSQL database for data persistence
- **Security**: Security groups for the application and database
- **Key_Pair**: SSH key pair for EC2 access
- **ECR**: Container registry (optional)

## Notes

1. This configuration creates resources that will incur AWS costs.
2. Remember to secure your database password in a production environment.
3. Consider setting up a proper state backend (S3 + DynamoDB) for team environments.
