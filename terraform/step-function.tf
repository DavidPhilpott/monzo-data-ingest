resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "monzo-data-ingest-state-machine"
  role_arn = aws_iam_policy.step_function_policy.arn
  depends_on = aws_iam_policy.step_function_policy

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


resource "aws_iam_policy" "step_function_policy" {
  name        = "step-function-policy"
  path        = "/monzo-data-ingest/"
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