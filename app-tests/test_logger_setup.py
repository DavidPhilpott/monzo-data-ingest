import app.logger_setup as logger_setup
import os
import mock
import logging
import pytest


@mock.patch.dict(os.environ, {'logging_level': 'INFO'})
def test_set_logger_level_passes_with_env_var():
    """Validate that the logger setup is valid given the correct os env"""
    logger = logging.getLogger("TestLogger")
    logger_setup.set_logger_level(logger)

    assert logger.getEffectiveLevel() == 20
    return


def test_set_logger_level_passes_with_no_env_var():
    """Validate that the logger setup is valid given the correct os env"""
    logger = logging.getLogger("TestLogger")
    logger_setup.set_logger_level(logger)

    assert logger.getEffectiveLevel() == 10
    return


@mock.patch.dict(os.environ, {'logging_level': 'RANDOM'})
def test_set_logger_level_raises_value_error_with_bad_env_var():
    """Validate that the logger setup is valid given the correct os env"""
    logger = logging.getLogger("TestLogger")
    with pytest.raises(ValueError):
        logger_setup.set_logger_level(logger)
    return
