resource "aws_lambda_function" "bootstrap_monzo_auth" {
  function_name = "monzo-data-ingest-bootstrap-auth-tokens"
  description   = "Echange a bootstrap token for initial access key and refresh token."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "bootstrap-auth.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  environment {
    variables = {
      client_id_parameter = aws_ssm_parameter.client_id.name,
      client_secret_id_parameter = aws_ssm_parameter.client_secret_id.name,
      access_key_parameter = aws_ssm_parameter.access_key.name,
      redirect_uri = aws_ssm_parameter.redirect_uri.name,
      refresh_token_parameter = aws_ssm_parameter.refresh_token.name,
      monzo_bootstrap_token_parameter = aws_ssm_parameter.monzo_bootstrap_token.name,
      logging_level = var.logging_level,
    }
  }

  tags = merge(
    {
      "Name" = "monzo-data-ingest-bootstrap-auth-tokens"
    },
    local.common_tags
  )
}