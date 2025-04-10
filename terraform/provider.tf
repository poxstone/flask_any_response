provider "google" {
  project = var.PROJECT_ID
  region  = var.REGION_DEFAULT
  zone    = local.ZONE
}
