aws_account_id = "020968065558"

region = "eu-west-1"

environment = "Prod"

project = "Monzo Data Ingest"

client_id = "oauth2client_00009jNbjw1TBhb75yrnlZ"

redirect_uri = "http://localhost:2020"

logging_level = "debug"

lambda_iam_actions = [
    "secretsmanager:List*",
    "secretsmanager:Get*",
    "ssm:Get*",
    "ssm:List*",
    "ssm:Put*"
  ]

lambda_iam_resources = [
  ]

lambda_timeout = 180

core_sns_arn_parameter = "core-message-inbox-arn"
core_sns_arn_parameter_arn = "arn:aws:ssm:eu-west-1:020968065558:parameter/core-message-inbox-arn"