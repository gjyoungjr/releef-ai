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
    subnets          = ["subnet-08f44ddd389841e62", "subnet-0ead33dd53ff8e157", "subnet-048bc660539c34193", "subnet-0385858ae166b9498"] # Replace "subnet-XXX" with your subnet IDs
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}




# resource "aws_ecs_task_definition" "hello_world" {
#   family                   = "hello-world-app"
#   network_mode             = "awsvpc"
#   requires_compatibilities = ["FARGATE"]
#   cpu                      = 1024
#   memory                   = 2048

#   container_definitions = <<DEFINITION
# [
#   {
#     "image": "registry.gitlab.com/architect-io/artifacts/nodejs-hello-world:latest",
#     "cpu": 1024,
#     "memory": 2048,
#     "name": "hello-world-app",
#     "networkMode": "awsvpc",
#     "portMappings": [
#       {
#         "containerPort": 3000,
#         "hostPort": 3000
#       }
#     ]
#   }
# ]
# DEFINITION
# }

# resource "aws_security_group" "hello_world_task" {
#   name   = "do4m-task-sg"
#   vpc_id = aws_vpc.default.id

#   ingress {
#     protocol        = "tcp"
#     from_port       = 3000
#     to_port         = 3000
#     security_groups = [aws_security_group.lb.id]
#   }

#   egress {
#     protocol    = "-1"
#     from_port   = 0
#     to_port     = 0
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

# resource "aws_ecs_cluster" "main" {
#   name = "do4m-cluster"
# }

# resource "aws_ecs_service" "hello_world" {
#   name            = "hello-world-service"
#   cluster         = aws_ecs_cluster.main.id
#   task_definition = aws_ecs_task_definition.hello_world.arn
#   desired_count   = var.app_count
#   launch_type     = "FARGATE"

#   network_configuration {
#     security_groups = [aws_security_group.hello_world_task.id]
#     subnets         = aws_subnet.private.*.id
#   }

#   load_balancer {
#     target_group_arn = aws_lb_target_group.hello_world.id
#     container_name   = "hello-world-app"
#     container_port   = 3000
#   }

#   depends_on = [aws_lb_listener.hello_world]
# }
