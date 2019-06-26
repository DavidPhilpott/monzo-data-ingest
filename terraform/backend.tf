terraform {
  backend "s3"{
    bucket = "master-backend-state"
    key = "monzo-data-ingest/state.tf"
    region = "eu-west-1"
  }
}