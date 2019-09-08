import boto3
import os
import logging
import app.logger_setup as logger_setup
import app.utilities as aws
from monzo import Monzo


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    logger_setup.set_logger_level(logger)
    logger_setup.set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    access_key = aws.get_ssm_parameter_value_from_env(parameter_name='access_key_parameter')
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
