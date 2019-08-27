//Incoming work queue for Monzo ingest jobs
resource "aws_sqs_queue" "work_entry_queue" {
  name                       = "monzo-data-ingest-inbound-work"
  delay_seconds              = 60
  receive_wait_time_seconds  = 10
  redrive_policy             = "{\"deadLetterTargetArn\":\"${aws_sqs_queue.master_dead_letter_queue.arn}\",\"maxReceiveCount\":3}"
  visibility_timeout_seconds = 300

  tags = merge(
    {
      "Name" = "monzo-data-ingest-inbound-work"
    },
    local.common_tags
  )
}

resource "aws_sqs_queue_policy" "work_entry_queue_policy" {
  queue_url = aws_sqs_queue.work_entry_queue.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.work_entry_queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:${var.region}:${var.aws_account_id}:core-message-inbox"
        }
      }
    }
  ]
}
POLICY
}

resource "aws_sns_topic_subscription" "sub-core-sns-to-monzo-work-entry-queue" {
  topic_arn = "arn:aws:sns:${var.region}:${var.aws_account_id}:core-message-inbox"
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.work_entry_queue.arn

  filter_policy = "{\"service\": [\"Monzo-Data-Ingest\"]}"
}

resource "aws_sqs_queue" "master_dead_letter_queue" {
  name                      = "monzo-data-ingest-dead-letter-queue"
  message_retention_seconds = 1209600 

  tags = merge(
    {
      "Name" = "monzo-data-ingest-dead-letter-queue"
    },
    local.common_tags
  )
}

resource "aws_sqs_queue_policy" "master_dead_letter_queue_policy" {
  queue_url = aws_sqs_queue.master_dead_letter_queue.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.master_dead_letter_queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sqs_queue.master_dead_letter_queue.arn}"
        }
      }
    }
  ]
}

POLICY
}