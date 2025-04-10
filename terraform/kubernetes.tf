
# kubernetes
resource "google_container_cluster" "gke_cluster1" {
  name                     = "gke-cluster-${var.PREFIX_APP}-01"
  location                 = local.ZONE
  remove_default_node_pool = true
  initial_node_count       = 1
  network                  = google_compute_network.custom_vpc_01.id
  subnetwork               = google_compute_subnetwork.subnet_gke_01.id
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
    tags         = []

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    #service_account = google_service_account.fla-na-a.email
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
    tags         = []

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    #service_account = google_service_account.fla-na-a.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  autoscaling {
    min_node_count = 0
    max_node_count = 20
  }
}
