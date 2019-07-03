resource "aws_sfn_state_machine" "sf_state_machine" {
  name     = "monzo-data-ingest-state-machine"
  role_arn = aws_iam_role.iam_for_sf.arn

  tags = merge(
    {
      "Name" = "monzo-data-ingest-state-machine"
    },
    local.common_tags
  )

  definition = <<EOF
  {
    "Comment": "Accesses Monzo account and ingests information from APIs.",
    "StartAt": "Check Access Key",
    "States": {
      "Check Access Key": {
        "Type": "Task",
        "Resource": "${aws_lambda_function.check_valid_auth_tokens.arn}",
        "Next": "Was Key Accepted?"
      },

      "Was Key Accepted?": {
        "Type": "Choice",
        "Choices": [
          {
            "Variable": "$.auth_granted",
            "BooleanEquals": false,
            "Next": "Refresh Access"
          },
          {
            "Variable": "$.auth_granted",
            "BooleanEquals": true,
            "Next": "Ingest Data"
          }
        ]
      },

      "Refresh Access": {
        "Type": "Task",
        "Resource": "${aws_lambda_function.refresh_auth_tokens.arn}",
        "Next": "Ingest Data"
      },

      "Ingest Data": {
        "Type": "Task",
        "Resource": "${aws_lambda_function.ingest_data.arn}",
        "End": "True"
      }
    }
  }
EOF
}

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


resource "aws_iam_role" "iam_for_sf" {
  name = "monzo-data-ingest-sf-role"

  assume_role_policy = data.aws_iam_policy_document.sf_assume_role_policy_document.json
}


data "aws_iam_policy_document" "sf_assume_role_policy_document" {

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

resource "aws_iam_role_policy" "sf_lambda_execution" {
  name = "monzo-data-ingest-sf-lambda-execution"
  role = aws_iam_role.iam_for_sf.id

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