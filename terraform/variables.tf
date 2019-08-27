variable aws_account_id {
  type = string
  description = "ID Number for the AWS Account."
}

variable project {
  type = string
  description = "Name of the project e.g. Monzo Data Ingest."
}

variable region {
  type = string
  description = "Region the porject is being built in."
}

locals {
  common_tags = {
      "Project"     = var.project
    }
}

variable client_id {
  type = string
  description = "Client ID of the Monzo service account."
}

variable redirect_uri {
  type = string
  description = "Registered Redirect URI for the Monzo service account."
}

## Lambdas

variable logging_level {
  type = string
  description = "The level the loggers will operate at within the Lambda functions."
}

variable core_sns_arn_parameter {
  type = string
  description = "Name of the parameter containg the Core SNS ARN."
}

variable core_sns_arn_parameter_arn {
  type = string
  description = "ARN of the parameter containging the core SNS ARN."
}