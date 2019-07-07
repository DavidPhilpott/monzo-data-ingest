resource "aws_lambda_function" "refresh_auth_tokens" {
  function_name = "monzo-data-ingest-refresh-auth-tokens"
  description   = "Exchanges current access key and refresh token for new ones."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "refresh_access.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  timeout = var.lambda_timeout

  environment {
    variables = {
      client_id_parameter = aws_ssm_parameter.client_id.name,
      client_secret_id_parameter = aws_ssm_parameter.client_secret_id.name,
      access_key_parameter = aws_ssm_parameter.access_key.name,
      refresh_token_parameter = aws_ssm_parameter.refresh_token.name,
      logging_level = var.logging_level,
    }
  }

  tags = merge(
    {
      "Name" = "monzo-data-ingest-refresh-auth-tokens"
    },
    local.common_tags
  )
}