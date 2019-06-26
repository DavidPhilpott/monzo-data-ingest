variable aws_account_id {
  type = string
}

variable project {
  type = string
}

variable environment {
  type = string
}

locals {
  common_tags = {
      "Project"     = var.project
      "Environment" = var.environment
    }
}