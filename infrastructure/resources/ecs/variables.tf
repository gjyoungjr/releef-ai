variable "service" {
  description = "The name of the service."
  type        = string
}

variable "private_subnet_ids" {
  description = "The IDs of the private subnets."
  type        = list(string)
}


variable "vpc_id" {
  description = "The ID of the VPC."
  type        = string

}
