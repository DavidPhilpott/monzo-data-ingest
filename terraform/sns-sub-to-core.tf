resource "aws_sns_topic_subscription" "sub-core-sns-to-monzo-work-entry-queue" {
  topic_arn = "arn:aws:sns:us-west-2:${aws_account_id}:core-message-inbox"
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.work_entry_queue.arn
}
