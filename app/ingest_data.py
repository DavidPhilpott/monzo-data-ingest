import boto3
import os
import logging


def set_logger_level(logger_to_set):
    """Get logging_level from environment and use to set the logging level."""
    logging_level = os.getenv('logging_level', 'NONE').upper()
    if logging_level is 'NONE':
        print("No logging_level environmental variable found. Defaulting to 'DEBUG'.")
        logging_level = 'DEBUG'
    else:
        print("Setting logger to level: %s." % logging_level)
    logging_level_name = logging.getLevelName(logging_level)
    logger_to_set.setLevel(logging_level_name)
    return


def set_logger_format(logger_to_format):
    """Set logger output format to a hardcoded version."""
    print("Setting logger formatting")
    log_format = logging.Formatter(fmt='%(asctime)s | %(levelname)s | %(message)s',
                                   datefmt='%d-%b-%y %H:%M:%S')
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(log_format)
    logger_to_format.addHandler(log_handler)
    return


def main(event, context):
    print("-- Instantiating logger --")
    global logger
    logger = logging.getLogger(__name__)
    logger.propagate = False
    set_logger_level(logger)
    set_logger_format(logger)

    logger.info("-- Getting Parameter Values --")
    access_key = get_ssm_parameter_value(parameter_name='access_key_parameter')
    logger.info("Finished getting parameter values.")
    logger.debug("Getting Monzo client.")
    monzo = Monzo(access_key)
    account_list = monzo_client.get_accounts()['accounts']
    print("Full account list")
    print(account_list)
    for account in account_list:
        account_id = account['id']
        print('id: %s, closed: %s' %(account['id'], account['closed']))
        balance = monzo.get_balance(account_id) # Get your balance object
        print("Balance:")
        print(balance['balance']) # 100000000000
        print("Currency:")
        print(balance['currency']) # GBP
        print("Spend Today:")
        print(balance['spend_today']) # 2000
        print("Transactions:")
        transactions = monzo.get_transactions(account_id)
        print(transactions)

    pots = monzo.get_pots()['pots']
    print("Pots:")
    print(pots)
    return