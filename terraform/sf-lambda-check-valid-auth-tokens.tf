resource "aws_lambda_function" "check_valid_auth_tokens" {
  function_name = "monzo-data-ingest-check-valid-auth-tokens"
  description   = "Tests if Monzo access key is still valid."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "test_authorisation.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  timeout = ${var.lambda_timeout}

  environment {
    variables = {
      access_key_parameter = aws_ssm_parameter.access_key.name,
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