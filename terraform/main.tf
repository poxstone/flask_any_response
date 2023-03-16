# BACKEND
# terraform backend saved state
#terraform {
#  backend "gcs" {
#    #bucket  = "PROJECT_ID"
#    bucket  = "__BACKEND_STATE__"
#    prefix  = "terraform/state"
#  }
#}

# VARIABLES
variable "PROJECT_ID" {default="PROJECT_ID"}
variable "REGION_DEFAULT" {default="us-east1"}
variable "ZONE_DEFAULT" {default="b"}
variable "PREFIX_APP" {default="flask"}
variable "SUBNET_RANGE_INFRA" {default="10.0.0.0/24"}
variable "SUBNET_RANGE_GKE" {default="10.100.0.0/20"}
variable "SUBNET_RANGE_PODS" {default="10.110.0.0/17"}
variable "SUBNET_RANGE_SERVICES" {default="10.120.0.0/22"}
locals {
  ZONE= "${var.REGION_DEFAULT}-${var.ZONE_DEFAULT}"
}

provider "google" {
  project     = var.PROJECT_ID
  region      = var.REGION_DEFAULT
  zone        = local.ZONE
}

# Networks
resource "google_compute_network" "custom_vpc_01" {
  name                    = "vpc-${var.PREFIX_APP}-01"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet_infra_01" {
  name          = "subnet-${var.PREFIX_APP}-infra-01"
  ip_cidr_range = var.SUBNET_RANGE_INFRA
  region        = var.REGION_DEFAULT
  network       = google_compute_network.custom_vpc_01.id
  private_ip_google_access   = true 
  depends_on = [ google_compute_network.custom_vpc_01]
}

resource "google_compute_subnetwork" "subnet_gke_01" {
  name          = "subnet-${var.PREFIX_APP}-gke-01"
  ip_cidr_range = var.SUBNET_RANGE_GKE
  region        = var.REGION_DEFAULT
  network       = google_compute_network.custom_vpc_01.id
  private_ip_google_access   = true 
  secondary_ip_range {
    range_name    = "subnet-gke-01-pods"
    ip_cidr_range = var.SUBNET_RANGE_PODS
  }
  secondary_ip_range {
    range_name    = "subnet-gke-01-services"
    ip_cidr_range = var.SUBNET_RANGE_SERVICES
  }
  depends_on = [ google_compute_network.custom_vpc_01]
}

# Firewall
resource "google_compute_firewall" "fw_allow_google_services" {
  network         = google_compute_network.custom_vpc_01.id
  name            = "${google_compute_network.custom_vpc_01.name}-allow-google-iap-lbs"
  source_ranges   = ["35.235.240.0/20", "35.191.0.0/16", "130.211.0.0/22", "209.85.152.0/22", "209.85.204.0/22", "169.254.169.254","130.211.0.0/22"]
  allow {
      protocol    = "all"
      ports       = []
  }
  depends_on = [ google_compute_network.custom_vpc_01]
}

resource "google_compute_firewall" "fw_allow_internal01" {
  network         = google_compute_network.custom_vpc_01.id
  name            = "${google_compute_network.custom_vpc_01.name}-allow-ingress-internal"
  source_ranges   = [var.SUBNET_RANGE_INFRA, var.SUBNET_RANGE_GKE, var.SUBNET_RANGE_PODS, var.SUBNET_RANGE_SERVICES]
  allow {
      protocol    = "all"
      ports       = []
  }
  depends_on = [google_compute_network.custom_vpc_01]
}


# kubernetes
resource "google_container_cluster" "gke_cluster1" {
  name     = "gke-cluster-${var.PREFIX_APP}-01"
  location = local.ZONE
  remove_default_node_pool = true
  initial_node_count       = 1
  network    = google_compute_network.custom_vpc_01.id
  subnetwork = google_compute_subnetwork.subnet_gke_01.id
  ip_allocation_policy {
    cluster_secondary_range_name  = google_compute_subnetwork.subnet_gke_01.secondary_ip_range.0.range_name
    services_secondary_range_name = google_compute_subnetwork.subnet_gke_01.secondary_ip_range.1.range_name
  }
  depends_on = [google_compute_subnetwork.subnet_gke_01]
}

resource "google_container_node_pool" "nodepool_preemptible_small" {
  name       = "nodepool-${var.PREFIX_APP}-e2-medium-preemptible"
  cluster    = google_container_cluster.gke_cluster1.id
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-medium"
    tags = []

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    #service_account = google_service_account.default.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  autoscaling {
      min_node_count = 0
      max_node_count = 20
  }
}

resource "google_container_node_pool" "nodepool_preemptible_small2" {
  name       = "nodepool-${var.PREFIX_APP}-e2-medium-preemptible2"
  cluster    = google_container_cluster.gke_cluster1.id
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-standard-2"
    tags = []

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    #service_account = google_service_account.default.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  autoscaling {
      min_node_count = 0
      max_node_count = 20
  }
}
