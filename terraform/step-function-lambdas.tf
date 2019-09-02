resource "aws_lambda_function" "refresh_auth_tokens" {
  function_name = "monzo-data-ingest-refresh-auth-tokens"
  description   = "Exchanges current access key and refresh token for new ones."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "refresh_access.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  timeout = 180

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

resource "aws_lambda_function" "ingest_data" {
  function_name = "monzo-data-ingest-ingest-data"
  description   = "Pull data from Monzo APIs."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "ingest_data.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]
  
  timeout = 180

  environment {
    variables = {
      access_key_parameter = aws_ssm_parameter.access_key.name,
      logging_level = var.logging_level,
    }
  }

  tags = merge(
    {
      "Name" = "monzo-data-ingest-ingest-data"
    },
    local.common_tags
  )
}

resource "aws_lambda_function" "check_valid_auth_tokens" {
  function_name = "monzo-data-ingest-check-valid-auth-tokens"
  description   = "Tests if Monzo access key is still valid."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "test_authorisation.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  timeout = 180

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

resource "aws_lambda_function" "ingest_account_data" {
  function_name = "monzo-data-ingest-ingest-account-data"
  description   = "Requests Monzo account data and writes to S3"
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "ingest_data_accounts.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  timeout = 180

  environment {
    variables = {
      data_lake_bucket_name = "dp-core-data-lake",
      environment = "prod",
      logging_level = var.logging_level,
      access_key_parameter = aws_ssm_parameter.access_key.name,
    }
  }

  tags = merge(
    {
      "Name" = "monzo-data-ingest-ingest-account-data"
    },
    local.common_tags
  )
}