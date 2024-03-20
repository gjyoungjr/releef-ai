
# IAM Role
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Role Policy
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Security group for the ECS tasks
resource "aws_security_group" "ecs_sg" {
  vpc_id = var.vpc_id
  name   = "ecs-security-group"
  # Inbound and outbound rules
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}



# ECS Cluster 
resource "aws_ecs_cluster" "cluster" {
  name = "${var.service}-cluster"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ECS service

resource "aws_ecs_service" "service" {
  name            = "${var.service}-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"


  # Network configuration
  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [aws_security_group.ecs_sg.id]
  }

}




resource "aws_ecs_task_definition" "task_definition" {
  family                   = "${var.service}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048

  # Task execution role 
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  # Container definition
  container_definitions = jsonencode([
    {
      name   = "${var.service}-container"
      image  = "public.ecr.aws/y9j1k7y7/nucleus:latest"
      cpu    = 256
      memory = 512
      port_mappings = [
        {
          container_port = 5000
          host_port      = 5000
          protocol       = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/${var.service}-task"
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "${var.service}-container"
          "awslogs-create-group"  = "true"
        }
      }
    }
  ])

}

