resource "aws_lb" "default" {
  name            = "${var.service}-lb"
  subnets         = var.public_subnet_ids
  security_groups = [var.security_group_id]
}

resource "aws_lb_target_group" "target_group" {
  name        = "${var.service}-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.default.id
  port              = "80"
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.target_group.id
    type             = "forward"
  }
}
