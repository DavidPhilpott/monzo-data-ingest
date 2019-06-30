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
  ]

lambda_iam_resources = [
    aws_ssm_parameter.client_id.arn,
    aws_ssm_parameter.redirect_uri.arn,
    aws_ssm_parameter.client_secret_id.arn,
    aws_ssm_parameter.access_key.arn,
    aws_ssm_parameter.refresh_token.arn,
]