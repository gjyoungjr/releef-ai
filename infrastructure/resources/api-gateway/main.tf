# API Gateway 
resource "aws_apigatewayv2_api" "api" {
  name          = "${var.service}-api-gateway"
  protocol_type = "HTTP"
}

# VPC Link 
resource "aws_apigatewayv2_vpc_link" "vpc_link" {
  name               = "${var.service}-vpclink"
  security_group_ids = [var.security_group_id]
  subnet_ids         = var.private_subnet_ids
}

# API Integration
resource "aws_apigatewayv2_integration" "api_integration" {
  api_id             = aws_apigatewayv2_api.api.id
  integration_type   = "HTTP_PROXY"
  connection_id      = var.vpc_id
  connection_type    = "VPC_LINK"
  description        = "VPC integration"
  integration_method = "ANY"
  integration_uri    = var.load_balancer_listener_arn
}

# APIGW Route
resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.api_integration.id}"
}
# APIGW Stage
resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}
