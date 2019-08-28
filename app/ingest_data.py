import boto3
import os
import logging
import app.logger_setup as logger_setup
from monzo import Monzo


def get_ssm_parameter_value(parameter_name):
    """Make a get request to SSM for the given parameter and return un-encrypted value"""
    logger.info("Seeking SSM value for environmental variable '%s'." % parameter_name)
    try:
        parameter_env = os.getenv(parameter_name, None)
        if parameter_env is not None:
            logger.debug("Found environmental variable. Associated value is set to '%s'" % parameter_env)
        else:
            raise ValueError("Could not find value for environmental variable '%s'" % parameter_name)
    except ValueError as e:
        logger.exception(e, exc_info=False)
        raise e
    logger.debug("Creating SSM client.")
    ssm_client = boto3.client('ssm')
    logger.debug("Requesting un-encrypted parameter information for '%s'." % parameter_env)
    parameter_info = ssm_client.get_parameter(Name=parameter_env, WithDecryption=True)
    logger.debug("Returned parameter_info dictionary. Seeking ['Parameter']['Value'].")
    parameter_value = parameter_info['Parameter']['Value']
    logger.info("Value found. Returning...")
    return parameter_value


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger_setup.set_logger_level(logger)
    logger_setup.set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    access_key = get_ssm_parameter_value(parameter_name='access_key_parameter')
    logger.info("Finished getting parameter values.")
    logger.debug("Getting Monzo client.")
    monzo_client = Monzo(access_key)
    account_list = monzo_client.get_accounts()['accounts']
    print("Full account list")
    print(account_list)
    for account in account_list:
        account_id = account['id']
        print('id: %s, closed: %s' %(account['id'], account['closed']))
        balance = monzo_client.get_balance(account_id) # Get your balance object
        print("Balance:")
        print(balance['balance']) # 100000000000
        print("Currency:")
        print(balance['currency']) # GBP
        print("Spend Today:")
        print(balance['spend_today']) # 2000
        print("Transactions:")
        transactions = monzo_client.get_transactions(account_id)
        print(transactions)

    pots = monzo_client.get_pots()['pots']
    print("Pots:")
    print(pots)
    return
