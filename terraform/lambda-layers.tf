resource "aws_lambda_layer_version" "monzo_requirements_lambda_layer" {
  filename   = "../app/requirements.zip"
  source_code_hash = "${filebase64sha256("../app/requirements.zip")}"
  layer_name = "monzo-data-ingest-requirements-lambda-layer"

  description = "Contains the library requirements for running Monzo Data Ingest lambda code."

  compatible_runtimes = ["python3.7"]
}
