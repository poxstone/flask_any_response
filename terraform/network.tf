
# Networks
resource "google_compute_network" "custom_vpc_01" {
  name                    = "vpc-${var.PREFIX_APP}-01"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet_infra_01" {
  name                     = "subnet-${var.PREFIX_APP}-infra-01"
  ip_cidr_range            = var.SUBNET_RANGE_INFRA
  region                   = var.REGION_DEFAULT
  network                  = google_compute_network.custom_vpc_01.id
  private_ip_google_access = true
  depends_on               = [google_compute_network.custom_vpc_01]
}

resource "google_compute_subnetwork" "subnet_gke_01" {
  name                     = "subnet-${var.PREFIX_APP}-gke-01"
  ip_cidr_range            = var.SUBNET_RANGE_GKE
  region                   = var.REGION_DEFAULT
  network                  = google_compute_network.custom_vpc_01.id
  private_ip_google_access = true
  secondary_ip_range {
    range_name    = "subnet-gke-01-pods"
    ip_cidr_range = var.SUBNET_RANGE_PODS
  }
  secondary_ip_range {
    range_name    = "subnet-gke-01-services"
    ip_cidr_range = var.SUBNET_RANGE_SERVICES
  }
  depends_on = [google_compute_network.custom_vpc_01]
}

# Firewall
resource "google_compute_firewall" "fw_allow_google_services" {
  network       = google_compute_network.custom_vpc_01.id
  name          = "${google_compute_network.custom_vpc_01.name}-allow-google-iap-lbs"
  source_ranges = ["35.235.240.0/20", "35.191.0.0/16", "130.211.0.0/22", "209.85.152.0/22", "209.85.204.0/22", "169.254.169.254", "130.211.0.0/22"]
  allow {
    protocol = "all"
    ports    = []
  }
  depends_on = [google_compute_network.custom_vpc_01]
}

resource "google_compute_firewall" "fw_allow_internal01" {
  network       = google_compute_network.custom_vpc_01.id
  name          = "${google_compute_network.custom_vpc_01.name}-allow-ingress-internal"
  source_ranges = [var.SUBNET_RANGE_INFRA, var.SUBNET_RANGE_GKE, var.SUBNET_RANGE_PODS, var.SUBNET_RANGE_SERVICES]
  allow {
    protocol = "all"
    ports    = []
  }
  depends_on = [google_compute_network.custom_vpc_01]
}

