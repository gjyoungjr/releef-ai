
variable "service" {
  type    = string
  default = "nucleus"
}

module "vpc" {
  source  = "./resources/vpc"
  service = var.service
}

module "load_balancer" {
  source            = "./resources/load-balancer"
  service           = var.service
  subnet_ids        = module.vpc.public_subnet_ids
  vpc_id            = module.vpc.vpc_id
  security_group_id = module.vpc.security_group_id

}




# # terraform {
# #   required_providers {
# #     aws = {
# #       source  = "hashicorp/aws"
# #       version = "~> 4.16"
# #     }
# #   }

# #   required_version = ">= 1.2.0"
# # }

# # # Provider definition
# # provider "aws" {
# #   region = "us-east-1"
# # }


# data "aws_availability_zones" "available_zones" {
#   state = "available"
# }

# # VPC definition
# data "aws_vpc" "existing" {
#   id = "vpc-0ba210283f5399e2d"
# }

# variable "cloudwatch_group" {
#   description = "CloudWatch group name."
#   type        = string
#   default     = "/ecs/nucleus-api-task"
# }


# # Security group for the ECS tasks
# resource "aws_security_group" "ecs_sg" {
#   vpc_id = data.aws_vpc.existing.id
#   name   = "ecs-security-group"
#   # Inbound and outbound rules
#   ingress {
#     from_port   = 5000
#     to_port     = 5000
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

# # IAM Role
# resource "aws_iam_role" "ecs_task_execution_role" {
#   name = "ecs-task-execution-role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow",
#         Principal = {
#           Service = "ecs-tasks.amazonaws.com"
#         },
#         Action = "sts:AssumeRole"
#       }
#     ]
#   })



# }

# # IAM Role Policy
# resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
#   role       = aws_iam_role.ecs_task_execution_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
# }


# # ECS task definition
# resource "aws_ecs_task_definition" "task_definition" {
#   family                   = "nucleus-api-task"
#   network_mode             = "awsvpc"
#   memory                   = "512"
#   requires_compatibilities = ["FARGATE"]

#   # Task execution role (Replace "XXX" with your IAM role ARN)
#   execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

#   # Container definition
#   container_definitions = jsonencode([
#     {
#       name   = "nucleus-api-container"
#       image  = "public.ecr.aws/y9j1k7y7/nucleus:latest"
#       cpu    = 256
#       memory = 512
#       port_mappings = [
#         {
#           container_port = 5000
#           host_port      = 5000
#           protocol       = "tcp"
#         }
#       ]
#       logConfiguration = {
#         logDriver = "awslogs"
#         options = {
#           "awslogs-group"         = "${var.cloudwatch_group}"
#           "awslogs-region"        = "us-east-1"
#           "awslogs-stream-prefix" = "nucleus-api-container"
#           "awslogs-create-group"  = "true"
#         }
#       }
#     }
#   ])

#   # Defining the task-level CPU
#   cpu = "256"
# }

# # ECS service
# resource "aws_ecs_cluster" "ecs_cluster" {
#   name = "nucleus-api-cluster"
#   setting {
#     name  = "containerInsights"
#     value = "enabled"
#   }
# }

# resource "aws_ecs_service" "service" {
#   name            = "nucleus-api-service"
#   cluster         = aws_ecs_cluster.ecs_cluster.id
#   task_definition = aws_ecs_task_definition.task_definition.arn
#   desired_count   = 1
#   launch_type     = "FARGATE"


#   # Network configuration
#   network_configuration {
#     subnets          = ["subnet-08f44ddd389841e62", "subnet-0ead33dd53ff8e157", "subnet-048bc660539c34193", "subnet-0385858ae166b9498"] # Replace "subnet-XXX" with your subnet IDs
#     security_groups  = [aws_security_group.ecs_sg.id]
#     assign_public_ip = true
#   }
# }
