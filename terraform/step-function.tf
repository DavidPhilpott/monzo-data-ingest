resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "monzo-data-ingest-state-machine"
  role_arn = "${aws_iam_role.iam_for_sfn.arn}"
  depends_on = [aws_iam_policy.step_function_policy]

  tags = merge(
    {
      "Name" = "monzo-data-ingest-state-machine"
    },
    local.common_tags
  )

  definition = <<EOF
{
  "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
  "StartAt": "HelloWorld",
  "States": {
    "HelloWorld": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.check_valid_auth_tokens.arn}",
      "End": true
    }
  }
}
EOF
}

resource "aws_iam_role" "step_function_role" {
  name = "monzo-data-ingest-step-function-role"

  assume_role_policy = aws_iam_policy.step_function_policy_document
}



// Assume role policy document
#data "aws_iam_policy_document" "sfn_assume_role_policy_document" {
#
#  statement {
#    actions = [
#      "sts:AssumeRole"
#    ]
#
#    principals {
#      type = "Service"
#      identifiers = [
#        "states.eu-west-1.amazonaws.com",
#        "events.amazonaws.com"
#      ]
#    }
#  }
#}

resource "aws_iam_policy" "step_function_policy" {
  name        = "monzo-data-ingest-step-function-policy"
  description = "Policy for the step function powering most of the monzo-data-ingest pipeline."

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
          "lambda:InvokeFunction"
      ],
      "Resource": [
          "arn:aws:lambda:${var.region}:${var.aws_account_id}:function:check_valid_auth_tokens"
      ]
    }
  ]
}
EOF
}








resource "aws_iam_role" "iam_for_lambda" {
  name = "tf-iam_for_lambda"

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

resource "aws_iam_role_policy" "dynamoDB-put" {
  name        = "tf-dynamoDB-put"
  role   = "${aws_iam_role.iam_for_lambda.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "dynamoDB:putItem"
      ],
      "Effect": "Allow",
      "Resource": "${aws_dynamodb_table.calculator-db.arn}"
    }
  ]
}
EOF
}


resource "aws_iam_role" "iam_for_sfn" {
  name = "tf-iam_for_sfn"

  assume_role_policy = "${data.aws_iam_policy_document.sfn_assume_role_policy_document.json}"
}



// Assume role policy document
data "aws_iam_policy_document" "sfn_assume_role_policy_document" {

  statement {
    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type = "Service"
      identifiers = [
        "states.eu-west-1.amazonaws.com",
        "events.amazonaws.com"
      ]
    }
  }
}



resource "aws_iam_role_policy" "lambda-execution" {
  name        = "tf-lambda-execution"
  role   = "${aws_iam_role.iam_for_sfn.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "lambda:InvokeFunction",
        "states:StartExecution"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}