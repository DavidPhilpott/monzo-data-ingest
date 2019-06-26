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
  queue_url = aws_sqs_queue.master_dead_letter_queue_policy.id

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