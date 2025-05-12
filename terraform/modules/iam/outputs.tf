output "ecs_task_execution_role" {
  description = "ARN of the ECS task execution role"
  value       = aws_iam_role.ecs_task_execution.arn
}

output "ecs_task_role" {
  description = "ARN of the ECS task role"
  value       = aws_iam_role.ecs_task.arn
}

output "ecs_instance_role" {
  description = "Name of the EC2 instance role for ECS"
  value       = aws_iam_role.ecs_instance_role.name
}
