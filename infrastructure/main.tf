
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
  public_subnet_ids = module.vpc.public_subnet_ids
  vpc_id            = module.vpc.vpc_id
  security_group_id = module.vpc.security_group_id

}

module "ecs" {
  source             = "./resources/ecs"
  service            = var.service
  private_subnet_ids = module.vpc.private_subnet_ids
  vpc_id             = module.vpc.vpc_id
}




