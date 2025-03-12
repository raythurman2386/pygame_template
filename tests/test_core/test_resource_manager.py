"""Test suite for the resource manager."""

import os
import pytest
import pygame
from src.core.resource_manager import ResourceManager


@pytest.fixture
def resource_manager():
    """Create a resource manager instance for testing."""
    return ResourceManager()


@pytest.fixture
def test_sound_path():
    """Get path to an existing test sound file."""
    return os.path.join("assets", "sounds", "ui_sounds", "click-a.ogg")


@pytest.fixture
def test_font_path():
    """Get path to an existing test font file."""
    return os.path.join("assets", "fonts", "kenney_future.ttf")


def test_resource_manager_initialization(resource_manager):
    """Test resource manager initialization."""
    assert resource_manager.images == {}
    assert resource_manager.sounds == {}
    assert resource_manager.fonts == {}


def test_load_nonexistent_image(resource_manager):
    """Test loading a non-existent image."""
    with pytest.raises(FileNotFoundError):
        resource_manager.load_image("nonexistent", "nonexistent.png")
    assert "nonexistent" not in resource_manager.images


def test_get_nonexistent_image(resource_manager):
    """Test retrieving a non-existent image."""
    image = resource_manager.get_image("nonexistent")
    assert image is None


def test_load_sound(resource_manager, test_sound_path):
    """Test loading a sound."""
    sound = resource_manager.load_sound("click", test_sound_path)
    assert sound is not None
    assert "click" in resource_manager.sounds


def test_get_sound(resource_manager, test_sound_path):
    """Test retrieving a loaded sound."""
    resource_manager.load_sound("click", test_sound_path)
    sound = resource_manager.get_sound("click")
    assert sound is not None


def test_load_font(resource_manager, test_font_path):
    """Test loading a font."""
    font = resource_manager.load_font("kenney", test_font_path, 24)
    assert font is not None
    assert ("kenney", 24) in resource_manager.fonts
    assert isinstance(font, pygame.font.Font)


def test_get_font(resource_manager, test_font_path):
    """Test retrieving a loaded font."""
    resource_manager.load_font("kenney", test_font_path, 24)
    font = resource_manager.get_font("kenney", 24)
    assert font is not None
    assert isinstance(font, pygame.font.Font)


def test_get_nonexistent_font(resource_manager):
    """Test retrieving a non-existent font."""
    font = resource_manager.get_font("nonexistent", 24)
    assert font is None
