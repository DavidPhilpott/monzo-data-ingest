resource "aws_ssm_parameter" "client_id" {
  name        = "monzo-data-ingest-client-id"
  description = "Client ID of the Monzo app which will be used to access the API."
  type        = "String"
  value       = var.client_id
  
  tags = merge(
    {
      "Name" = "monzo-data-ingest-client-id"
    },
    local.common_tags
  )
}

resource "aws_ssm_parameter" "redirect_uri" {
  name        = "monzo-data-ingest-redirect-uri"
  description = "Redirect URI that the monzo app is allowed to feed back to."
  type        = "String"
  value       = var.redirect_uri
  
  tags = merge(
    {
      "Name" = "monzo-data-ingest-redirect-uri"
    },
    local.common_tags
  )
}

resource "aws_ssm_parameter" "client_secret_id" {
  name        = "monzo-data-ingest-client-secret-id"
  description = "Secret ID of the Monzo app which will be used to access the API."
  type        = "SecureString"
  value       = "xyz"
  overwrite   = false

  lifecycle {
    ignore_changes = [
      value,
  ]

  tags = merge(
    {
      "Name" = "monzo-data-ingest-client-secret-id"
    },
    local.common_tags
  )

}

resource "aws_ssm_parameter" "access_key" {
  name        = "monzo-data-ingest-access-key"
  description = "Access key used to request from the API."
  type        = "SecureString"
  value       = "xyz"
  overwrite   = false

  lifecycle {
    ignore_changes = [
      value,
  ]

  tags = merge(
    {
      "Name" = "monzo-data-ingest-access-key"
    },
    local.common_tags
  )

}

resource "aws_ssm_parameter" "refresh_token" {
  name        = "monzo-data-ingest-refresh-token"
  description = "Refresh token used to renew the Monzo access key."
  type        = "SecureString"
  value       = "xyz"
  overwrite   = false

  tags = merge(
    {
      "Name" = "monzo-data-ingest-refresh-token"
    },
    local.common_tags
  )

  lifecycle {
    ignore_changes = [
      value,
  ]

}