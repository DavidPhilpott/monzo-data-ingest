resource "aws_lambda_function" "check_valid_auth_tokens" {
  function_name = "monzo-data-ingest-check-valid-auth-tokens"
  description   = "Tests if Monzo access key is still valid and regenerates if not."
  role          = aws_iam_role.iam_role_check_valid_auth_tokens_lambda.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "test_and_regenerate_auth.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

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


## EC2 Access Policy

data "aws_iam_policy_document" "monzo_lambda_ec2_policy_document" {
  statement {
    actions = [
      "ec2:CreateNetworkInterface",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DeleteNetworkInterface"
    ]

    resources = [
      "*"
    ]
  } 
}

resource "aws_iam_role_policy" "monzo_lambda_ec2_policy" {
  role   = aws_iam_role.iam_role_check_valid_auth_tokens_lambda.id
  policy = data.aws_iam_policy_document.monzo_lambda_ec2_policy_document.json
}

## Other Access Policy

data "aws_iam_policy_document" "monzo_lambda_custom_policy_document" {
  statement {
    actions   = var.lambda_iam_actions
    resources = concat(
      [
        aws_ssm_parameter.client_id.arn,
        aws_ssm_parameter.redirect_uri.arn,
        aws_ssm_parameter.client_secret_id.arn,
        aws_ssm_parameter.access_key.arn,
        aws_ssm_parameter.refresh_token.arn,
      ],
      var.lambda_iam_resources,
    )
  }
}

resource "aws_iam_role_policy" "monzo_lambda_custom_policy" {
  role   = aws_iam_role.iam_role_check_valid_auth_tokens_lambda.id
  policy = data.aws_iam_policy_document.monzo_lambda_custom_policy_document.json
}