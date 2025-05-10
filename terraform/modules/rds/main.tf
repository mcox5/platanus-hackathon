resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-db-subnet-group-${var.environment}"
  subnet_ids = var.private_subnet_ids
  
  tags = {
    Name        = "${var.app_name}-db-subnet-group-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_db_instance" "main" {
  identifier              = "${var.app_name}-db-${var.environment}"
  allocated_storage       = var.db_allocated_storage
  storage_type            = "gp2"
  engine                  = "postgres"
  engine_version          = "15"
  instance_class          = var.db_instance_class
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [var.db_security_group_id]
  skip_final_snapshot     = true
  backup_retention_period = 7
  multi_az                = var.environment == "prod" ? true : false
  
  tags = {
    Name        = "${var.app_name}-db-${var.environment}"
    Environment = var.environment
  }
}
