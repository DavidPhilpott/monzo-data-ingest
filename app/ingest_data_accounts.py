import logging
import boto3
import logger_setup as logger_setup
import utilities as aws
import os
import json
from monzo import Monzo

global logger
logger = logging.getLogger(__name__)
logger.propagate = False
logger_setup.set_logger_level(logger)
logger_setup.set_logger_format(logger)


def get_monzo_client(access_key):
    """Create a Monzo client object"""
    logger.info("Creating Monzo client object.")
    monzo_client = Monzo(access_key)
    logger.info("Client created. Returning.")
    return monzo_client


def get_account_data(monzo_client):
    """Request the account data for a Monzo client"""
    logger.info("Requesting account data")
    account_data = monzo_client.get_accounts()
    logger.info("Account data found. Returning.")
    logger.debug("Account data is: %s" % account_data)
    return account_data


def get_account_list(account_data):
    """Parse out account list from raw account data"""
    logger.info("Extracting account list from account data.")
    account_list = account_data["accounts"]
    logger.info("Account list extracted. Returning.")
    logger.debug("Account list is: %s" % account_list)
    return account_list


def build_data_lake_target_path(project, environment, date, filename):
    """Create the path that the data will be dumped to in S3"""
    logger.info("Building target data lake path.")
    logger.debug("Path components are: project=%s, environment=%s, date=%s, filename=%s" %
                 (project, environment, date, filename))
    target_path = project + "/" + environment + "/" + date + "/" + filename
    logger.info("Target path build. Returning.")
    logger.debug("Target path is %s." % target_path)
    return target_path


def get_s3_client():
    """Wrapper for getting an S3 client via boto3"""
    logger.info("Requesting an S3 client.")
    s3_client = boto3.client("s3")
    logger.info("Got client. Returning.")
    return s3_client


def write_data_to_s3(s3_client, bucket_name, target_path, data_to_write):
    """Write the given data to the target path in S3"""
    logger.info("Writing data to S3.")
    logger.debug("Bucket name is %s. Target path is %s" % (bucket_name, target_path))
    s3_client.put_object(Body=data_to_write,
                         Bucket=bucket_name,
                         Key=target_path)
    logger.info("Completed writing to s3. Returning.")
    return


def main(event, context):
    logger.info("-- Getting Parameter Values --")
    access_key = aws.get_ssm_parameter_value_from_env(parameter_name='access_key_parameter')
    data_lake_bucket = os.getenv("data_lake_bucket_name")
    batch_date = event['date_to_process']
    environment = os.getenv("environment")
    logger.info("Finished getting parameter values.")

    logger.info("-- Ingesting Account Data --")
    monzo_client = get_monzo_client(access_key)
    account_data = get_account_data(monzo_client)
    data_target_path = build_data_lake_target_path(project="monzo",
                                                   environment=environment,
                                                   date=batch_date,
                                                   filename="account-data.json")
    s3_client = get_s3_client()
    write_data_to_s3(s3_client=s3_client,
                     bucket_name=data_lake_bucket,
                     target_path=data_target_path,
                     data_to_write=json.dumps(account_data))
    logger.info("Finished ingesting account data.")

    logger.info("Extracting and passing on account list.")
    account_list = get_account_list(account_data)
    logger.debug("Account list is %s" % account_list)
    logger.info("Complete.")
    return account_list

