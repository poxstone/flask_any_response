# VARIABLES
variable "PROJECT_ID" { default = "PROJECT_ID" }
variable "REGION_DEFAULT" { default = "us-east1" }
variable "ZONE_DEFAULT" { default = "b" }
variable "PREFIX_APP" { default = "flask" }
variable "SUBNET_RANGE_INFRA" { default = "10.0.0.0/24" }
variable "SUBNET_RANGE_GKE" { default = "10.100.0.0/20" }
variable "SUBNET_RANGE_PODS" { default = "10.110.0.0/17" }
variable "SUBNET_RANGE_SERVICES" { default = "10.120.0.0/22" }
locals {
  ZONE = "${var.REGION_DEFAULT}-${var.ZONE_DEFAULT}"
}

