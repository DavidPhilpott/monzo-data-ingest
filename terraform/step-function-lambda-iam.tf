//Blanket role used by Monzo lambdas to access SQS / SNS / SF objects and execute.
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

  statement {
    actions = [
      "sns:Publish",
      "sns:Subscribe",
    ]
    resources = [
      "*",
    ]
  }

  statement {
    actions = [
      "sqs:ChangeMessageVisibility",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ReceiveMessage",
    ]
    resources = [
      "*",
    ]
  }

  statement {
    actions = [
      "states:StartExecution"
    ]
    resources = [
      "*"
    ]

  statement {
    actions = [
      "s3:*"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_role_policy" "monzo_lambda_core_policy" {
  role   = aws_iam_role.iam_role_lambdas.id
  policy = data.aws_iam_policy_document.monzo_lambda_core_policy_document.json
}

data "aws_iam_policy_document" "monzo_lambda_custom_policy_document" {
  statement {
    actions = [
      "secretsmanager:List*",
      "secretsmanager:Get*",
      "ssm:Get*",
      "ssm:List*",
      "ssm:Put*",
    ]
    resources = [
      aws_ssm_parameter.client_id.arn,
      aws_ssm_parameter.redirect_uri.arn,
      aws_ssm_parameter.client_secret_id.arn,
      aws_ssm_parameter.access_key.arn,
      aws_ssm_parameter.refresh_token.arn,
      aws_ssm_parameter.monzo_bootstrap_token.arn,
      var.core_sns_arn_parameter_arn,
    ]
  }
}

resource "aws_iam_role_policy" "monzo_lambda_custom_policy" {
  role   = aws_iam_role.iam_role_lambdas.id
  policy = data.aws_iam_policy_document.monzo_lambda_custom_policy_document.json
}