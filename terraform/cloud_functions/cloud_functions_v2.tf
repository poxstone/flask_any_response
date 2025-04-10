locals {
  fc_prefix_name = "gcf-tf-any-response"
  str_date       = formatdate("YYMMDDhhmmss", timestamp())
  source_path    = "../../"
  bucket         = "p4-operations-dev-gcf-source"
  project = "p4-operations-dev"
}

data "archive_file" "zip_cloud_function" {
  type        = "zip"
  source_dir  = local.source_path
  output_path = "${local.fc_prefix_name}.zip"
  excludes = [
    "kubernetes*",
    "terraform*",
    "nginx*",
    "jmeter*",
    "openapi*",
    "venv",
    "helm",
    "*.tf",
    "*.yaml",
    "*.pyc",
    "application/__pycache__",
    "cloudrun",
    "api_gateway",
    ".git*",
    ".doc*",
    ".gcl*",
    ".vscode",
    "README.md",
    "curl_tests",
  ]
}


resource "google_storage_bucket_object" "obj_function" {
  name       = "${local.fc_prefix_name}.zip#${data.archive_file.zip_cloud_function.output_md5}"
  bucket     = local.bucket
  source     = data.archive_file.zip_cloud_function.output_path
  depends_on = [data.archive_file.zip_cloud_function]
}

resource "google_cloudfunctions2_function" "function" {
  name        = "gcf-tf-flask-any-response"
  location    = "us-central1"
  description = "test function"
  project     = local.project

  build_config {
    runtime     = "python311"
    entry_point = "functions_trigger" # Set the entry point 
    source {
      storage_source {
        bucket = google_storage_bucket_object.obj_function.bucket
        object = google_storage_bucket_object.obj_function.name
      }
    }
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 60
  }

  depends_on = [resource.google_storage_bucket_object.obj_function]
}
