# Terraform Infrastructure for Platanus App

This directory contains Terraform configuration to deploy the Platanus application on AWS. The architecture uses AWS services without EKS as requested, instead utilizing ECS Fargate for containerized applications and RDS for database hosting.

## Architecture Overview

The infrastructure consists of the following components:

- **VPC**: A secure network environment with public and private subnets across multiple availability zones
- **ECS Fargate**: Serverless compute platform for running containerized applications
- **RDS PostgreSQL**: Managed relational database service for PostgreSQL
- **ECR**: Container registry for storing Docker images
- **ALB**: Application Load Balancer for routing traffic to the application
- **IAM Roles**: Proper permissions for ECS tasks and services
- **CloudWatch**: Logging and monitoring

## Prerequisites

1. AWS CLI installed and configured
2. Terraform installed (v1.0 or later)
3. Docker installed (for building and pushing container images)

## How to Deploy

1. **Initialize Terraform:**
   ```
   cd terraform
   terraform init
   ```

2. **Create a terraform.tfvars file:**
   Create a file named `terraform.tfvars` with the following variables:
   ```
   aws_region           = "us-east-1"
   app_name             = "platanus-app"
   environment          = "prod"
   db_name              = "appdb"
   db_username          = "postgres"
   db_password          = "your-secure-password"
   db_instance_class    = "db.t3.micro"
   db_allocated_storage = 20
   ```

3. **Plan the deployment:**
   ```
   terraform plan -out=tfplan
   ```

4. **Apply the configuration:**
   ```
   terraform apply tfplan
   ```

5. **Build and push the Docker image:**
   After the infrastructure is deployed, you need to build and push your Docker image to the created ECR repository:
   ```bash
   # Get the ECR repository URL
   ECR_REPO=$(terraform output -raw ecr_repository_url)
   
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_REPO
   
   # Build the image
   docker build -t $ECR_REPO:latest ..
   
   # Push the image
   docker push $ECR_REPO:latest
   ```

6. **Refresh the ECS service to deploy the new image:**
   ```bash
   CLUSTER_NAME=$(terraform output -raw ecs_cluster_name)
   SERVICE_NAME=$(terraform output -raw ecs_service_name)
   
   aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --force-new-deployment
   ```

## Accessing the Application

After the deployment is complete, you can access the application using the ALB DNS name:

```
ALB_DNS=$(terraform output -raw alb_dns_name)
echo "Application URL: http://$ALB_DNS"
```

## Cleanup

To destroy the infrastructure when no longer needed:

```
terraform destroy
```

## Modules Overview

The infrastructure is organized into the following modules:

- **VPC**: Network infrastructure
- **RDS**: PostgreSQL database
- **Security**: Security groups for the application, ALB, and database
- **ECR**: Container registry
- **ECS**: Container service and load balancer
- **IAM**: Roles and policies for the services

## Notes

1. This configuration creates resources that will incur AWS costs.
2. Remember to secure your database password in a production environment.
3. Consider setting up a proper state backend (S3 + DynamoDB) for team environments.
