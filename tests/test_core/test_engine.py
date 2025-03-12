"""Test suite for the game engine core."""

import pytest
import pygame
from src.core.engine import Engine
from src.utils.logger import GameLogger


def test_engine_initialization(mock_engine):
    """Test basic engine initialization."""
    assert mock_engine.width == 800
    assert mock_engine.height == 600
    assert mock_engine.title == "Test Engine"
    assert mock_engine.fps == 60
    assert not mock_engine.running
    assert isinstance(mock_engine.logger, GameLogger._loggers["Engine"].__class__)


def test_engine_settings(mock_engine):
    """Test engine settings initialization."""
    assert mock_engine.settings.music_enabled is True
    assert mock_engine.settings.sfx_enabled is True
    assert mock_engine.settings.music_volume == 0.5
    assert mock_engine.settings.master_volume == 1.0
    assert mock_engine.settings.fullscreen is False


def test_debug_logging_toggle(mock_engine):
    """Test debug logging toggle functionality."""
    initial_level = mock_engine.logger.level
    mock_engine.toggle_debug_logging()
    assert mock_engine.debug_logging is True
    assert mock_engine.logger.level != initial_level

    mock_engine.toggle_debug_logging()
    assert mock_engine.debug_logging is False
    assert mock_engine.logger.level == initial_level


def test_event_handling(mock_engine, monkeypatch):
    """Test event handling with F1/F2 keys."""
    # Mock pygame.event.get to return our test events
    events = [
        pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F1}),
        pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_F2}),
    ]
    monkeypatch.setattr(pygame.event, "get", lambda: events)

    # Store initial states
    initial_debug = mock_engine.debug_logging

    # Handle events
    mock_engine.handle_events()

    # Verify debug logging was toggled
    assert mock_engine.debug_logging != initial_debug
    # Engine should still be running as we didn't send a QUIT event
    assert not mock_engine.running


@pytest.fixture
def mock_pygame_quit(mocker):
    """Mock pygame.quit to avoid actual cleanup."""
    return mocker.patch("pygame.quit")
