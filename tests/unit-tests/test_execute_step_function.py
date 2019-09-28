import mock
import app.execute_step_function as execute_step_function
import json
from freezegun import freeze_time


def test_extract_date_to_process_from_message_pass():
    """Pass through a valid message structure and extract the date"""
    test_date = 'YYYY-MM-DD'
    test_message_attributes = json.dumps({'MessageAttributes': {'date_to_process': {'Value': test_date}}})
    test_event_message = {'Records': [{'body': test_message_attributes}]}
    extracted_date = execute_step_function.extract_date_to_process_from_message(event_message=test_event_message)
    assert extracted_date == test_date
    return


def test_build_step_function_input_json_pass():
    """Pass a valid date into the function and receive the correct dictionary format"""
    test_date = 'YYYY-MM-DD'
    valid_output = {'date_to_process': 'YYYY-MM-DD'}
    test_output = execute_step_function.build_step_function_input_json(date_to_process=test_date)
    assert test_output == valid_output
    return


def test_generate_execution_name():
    """Pass through date to process and get back valid result"""
    test_date = 'YYYY-MM-DD'
    valid_output = "Monzo-Data-Ingest-YYYY-MM-DD-19851204000000"
    with freeze_time("1985-12-04"):
        test_output = execute_step_function.generate_execution_name(date_to_process=test_date)
        assert test_output == valid_output
    return
