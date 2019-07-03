resource "aws_iam_role" "iam_role_lambdas" {
  name = "lambda-role-monzo-data-ingest"

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

data "aws_iam_policy_document" "monzo_lambda_core_policy_document" {
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

  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      "arn:aws:logs:${var.region}:${var.aws_account_id}:*"
    ]
}
}

resource "aws_iam_role_policy" "monzo_lambda_core_policy" {
  role   = aws_iam_role.iam_role_check_valid_auth_tokens_lambda.id
  policy = data.aws_iam_policy_document.monzo_lambda_core_policy_document.json
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