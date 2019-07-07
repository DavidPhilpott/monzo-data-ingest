resource "aws_lambda_function" "ingest_data" {
  function_name = "monzo-data-ingest-ingest-data"
  description   = "Pull data from Monzo APIs."
  role          = aws_iam_role.iam_role_lambdas.arn

  runtime           = "python3.7"
  filename          = "../app/app.zip"
  source_code_hash  = "${filebase64sha256("../app/app.zip")}"
  handler           = "ingest_data.main"
  layers            = [aws_lambda_layer_version.monzo_requirements_lambda_layer.arn]

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