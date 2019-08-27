//Lambda function running on a cron that pushes Monzo Ingest jobs to the central SNS
resource "aws_lambda_function" "job_trigger_lambda" {
  function_name = "monzo-data-ingest-job-trigger"
  description   = "Pushes Monzo jobs to core SNS based on cron."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "trigger_job.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

  timeout = 180

  environment {
    variables = {
      target_sns_arn_parameter = var.core_sns_arn_parameter,
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

resource "aws_cloudwatch_event_rule" "monzo_trigger_once_per_day" {
    name = "monzo-trigger-once-per-day"
    description = "Cron job executing Monzo Data Ingest once per day (8am)"
    schedule_expression = "cron(0 8 * * ? *)"
}

resource "aws_cloudwatch_event_target" "trigger_job_trigger_lambda_on_cron" {
    rule = "${aws_cloudwatch_event_rule.monzo_trigger_once_per_day.name}"
    target_id = "job_trigger_lambda"
    arn = "${aws_lambda_function.job_trigger_lambda.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.job_trigger_lambda.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.monzo_trigger_once_per_day.arn}"
}