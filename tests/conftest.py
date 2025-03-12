"""Common test fixtures and configurations."""

import pytest
import pygame
from src.core.engine import Engine
from src.utils.logger import GameLogger


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame for all tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def test_logger():
    """Create a test logger instance."""
    return GameLogger.get_logger("TestLogger", log_to_file=False, log_to_console=True)


@pytest.fixture
def mock_engine():
    """Create a mock game engine instance."""
    engine = Engine(width=800, height=600, title="Test Engine")
    return engine
