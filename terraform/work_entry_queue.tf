resource "aws_sqs_queue" "work_entry_queue" {
  name                      = "monzo-data-ingest-inbound-work"
  delay_seconds             = 60
  receive_wait_time_seconds = 10
  redrive_policy            = "{\"deadLetterTargetArn\":\"${aws_sqs_queue.master_dead_letter_queue.arn}\",\"maxReceiveCount\":3}"

  tags = merge(
    {
      "Name" = aws_sqs_queue.work_entry_queue.name
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
          "aws:SourceArn": "${aws_sqs_queue.work_entry_queue.arn}"
        }
      }
    }
  ]
}
POLICY
}
