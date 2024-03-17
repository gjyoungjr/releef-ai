variable "service" {
  description = "The name of the service."
  type        = string
}

variable "public_subnet_ids" {
  description = "The IDs of the public subnets."
  type        = list(string)
}

variable "security_group_id" {
  description = "The ID of the security group."
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC."
  type        = string

}
