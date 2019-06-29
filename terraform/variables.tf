variable aws_account_id {
  type = string
}

variable project {
  type = string
}

variable environment {
  type = string
}

variable region {
  type = string
}

locals {
  common_tags = {
      "Project"     = var.project
      "Environment" = var.environment
    }
}

variable client_id {
  type = string
}

variable redirect_uri {
  type = string
}