resource "aws_lambda_function" "check_valid_auth_tokens" {
  filename      = "../app/app.zip"
  function_name = "monzo-data-ingest-check-valid-auth-tokens"
  role          = aws_iam_role.iam_role_check_valid_auth_tokens_lambda.arn
  handler       = "exports.test"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = "${filebase64sha256("../app/app.zip")}"

  runtime = "python3.7"

  environment {
    variables = {
      client_id_parameter = aws_ssm_parameter.client_id.name,
      client_secret_id_parameter = aws_ssm_parameter.client_secret_id.name,
      redirect_uri_parameter = aws_ssm_parameter.redirect_uri.name,
      access_key_parameter = aws_ssm_parameter.access_key.name,
      refresh_token_parameter = aws_ssm_parameter.refresh_token.name,
      logging_level = var.logging_level,
    }
  }

  tags = merge(
    {
      "Name" = "monzo-data-ingest-check-valid-auth-tokens"
    },
    local.common_tags
  )
}

resource "aws_iam_role" "iam_role_check_valid_auth_tokens_lambda" {
  name = "lambda-role-monzo-data-ingest-check-valid-auth-tokens"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

