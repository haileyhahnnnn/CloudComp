## Google Groups here
# Deploying Google Groups through terraform 

# Enabling required APIs 
resource "google_project_service" "identity_api" {
  project = "your-project-id"
  service = "cloudidentity.googleapis.com"
}

# Create a cloud identity group 
resource "google_cloud_identity_group" "example_group" {
  provider = google-beta
  display_name = "Engineering Team"
  group_key {
    id = "engineering@example.com"
  }
  labels = {
    "cloudidentity.googleapis.com/groups.discussion_forum" = ""
  }
}

# Adding IAM members to the group 
resource "google_cloud_identity_group_membership" "example_membership" {
  provider = google-beta
  group = google_cloud_identity_group.example_group.id
  preferred_member_key {
    id = "user1@example.com"
  }
  roles = ["MEMBER"]
}

# Assign IAM permissions to the group 
resource "google_project_iam_binding" "group_binding" {
  project = "your-project-id"
  role    = "enter roles/editor here"
  members = [
    "group:engineering@example.com"
  ]
}
