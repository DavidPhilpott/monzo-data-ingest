//Creates a Lambda and cront job that push job notifciations onto the core SNS to trigger Monzo jobs

resource "aws_lambda_function" "step_function_executor_lambda" {
  function_name = "monzo-data-ingest-step-function-executor"
  description   = "Starts execution of Monzo step function based on incoming SQS items."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "execute_step_function.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  timeout = var.lambda_timeout

  environment {
    variables = {
      target_step_function_arn = aws_sfn_state_machine.sf_state_machine.id,
      logging_level = var.logging_level,
    }
  }

  tags = merge(
    {
      "Name" = "monzo-data-ingest-job-trigger"
    },
    local.common_tags
  ) 
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
  event_source_arn = aws_sqs_queue.work_entry_queue.arn
  enabled          = true
  function_name    = aws_lambda_function.step_function_executor_lambda.arn
  batch_size       = 1

  depends_on = [aws_iam_role.iam_role_lambdas, aws_iam_role_policy.monzo_lambda_core_policy]
}