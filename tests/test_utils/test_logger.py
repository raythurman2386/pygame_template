"""Test suite for the game logger."""

import os
import logging
import pytest
from src.utils.logger import GameLogger


@pytest.fixture
def temp_log_dir(tmp_path):
    """Create a temporary log directory."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return str(log_dir)


@pytest.fixture
def test_logger(temp_log_dir):
    """Create a test logger instance."""
    return GameLogger.get_logger(
        "TestLogger",
        level=logging.DEBUG,
        log_to_file=True,
        log_to_console=True,
        file_path=os.path.join(temp_log_dir, "test.log"),
    )


def test_logger_initialization(test_logger):
    """Test logger initialization."""
    assert test_logger.name == "TestLogger"
    assert test_logger.level == logging.DEBUG
    assert len(test_logger.handlers) > 0


def test_logger_singleton():
    """Test logger singleton pattern."""
    logger1 = GameLogger.get_logger("SingletonTest")
    logger2 = GameLogger.get_logger("SingletonTest")
    assert logger1 is logger2


def test_logger_levels(test_logger):
    """Test different logging levels."""
    test_logger.debug("Debug message")
    test_logger.info("Info message")
    test_logger.warning("Warning message")
    test_logger.error("Error message")
    test_logger.critical("Critical message")

    # If we got here without exceptions, test passes
    assert True


def test_set_all_loggers_level():
    """Test setting level for all loggers."""
    logger1 = GameLogger.get_logger("Logger1")
    logger2 = GameLogger.get_logger("Logger2")

    GameLogger.set_all_loggers_level(logging.ERROR)

    assert logger1.level == logging.ERROR
    assert logger2.level == logging.ERROR


def test_logger_file_handler(temp_log_dir):
    """Test logger file handler creation."""
    log_file = os.path.join(temp_log_dir, "file_test.log")
    logger = GameLogger.get_logger("FileTest", log_to_file=True, file_path=log_file)

    test_message = "Test log message"
    logger.info(test_message)

    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        content = f.read()
        assert test_message in content


def test_logger_console_only():
    """Test logger with console output only."""
    logger = GameLogger.get_logger("ConsoleTest", log_to_file=False, log_to_console=True)

    # Check that we only have one handler (StreamHandler)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_logger_thread_safety(test_logger):
    """Test logger thread safety."""
    import threading

    def log_messages():
        for i in range(100):
            test_logger.info(f"Thread message {i}")

    threads = [threading.Thread(target=log_messages) for _ in range(5)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # If we got here without exceptions, test passes
    assert True
