output "public_subnet_ids" {
  value = aws_subnet.public.*.id
}

output "vpc_id" {
  value = aws_vpc.default.id
}

output "security_group_id" {
  value = aws_security_group.security_group.id
}
