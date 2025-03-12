"""Test suite for the scene manager."""

import pytest
import pygame
from src.core.scene_manager import SceneManager
from src.scenes.scene import Scene


class MockScene(Scene):
    """Mock scene for testing."""

    def __init__(self):
        self.entered = False
        self.exited = False
        self.event_handled = False
        self.updated = False
        self.rendered = False

    def enter(self):
        self.entered = True

    def exit(self):
        self.exited = True

    def handle_event(self, event):
        self.event_handled = True

    def update(self, dt):
        self.updated = True

    def render(self, surface):
        self.rendered = True


@pytest.fixture
def scene_manager(mock_engine):
    """Create a scene manager instance for testing."""
    return SceneManager(mock_engine)


@pytest.fixture
def mock_scene():
    """Create a mock scene for testing."""
    return MockScene()


def test_scene_manager_initialization(scene_manager):
    """Test scene manager initialization."""
    assert scene_manager.scenes == {}
    assert scene_manager.current_scene is None
    assert scene_manager.current_scene_name is None


def test_add_scene(scene_manager, mock_scene):
    """Test adding a scene."""
    scene_manager.add_scene("test_scene", mock_scene)
    assert "test_scene" in scene_manager.scenes
    assert scene_manager.scenes["test_scene"] == mock_scene


def test_switch_scene(scene_manager, mock_scene):
    """Test switching between scenes."""
    scene_manager.add_scene("test_scene", mock_scene)
    scene_manager.switch_to("test_scene")

    assert scene_manager.current_scene == mock_scene
    assert scene_manager.current_scene_name == "test_scene"
    assert mock_scene.entered


def test_switch_scene_with_exit(scene_manager):
    """Test switching scenes triggers exit on current scene."""
    first_scene = MockScene()
    second_scene = MockScene()

    scene_manager.add_scene("first", first_scene)
    scene_manager.add_scene("second", second_scene)

    scene_manager.switch_to("first")
    scene_manager.switch_to("second")

    assert first_scene.exited
    assert second_scene.entered


def test_invalid_scene_switch(scene_manager):
    """Test switching to non-existent scene raises error."""
    with pytest.raises(ValueError):
        scene_manager.switch_to("non_existent_scene")


def test_scene_event_handling(scene_manager, mock_scene):
    """Test event handling in current scene."""
    scene_manager.add_scene("test_scene", mock_scene)
    scene_manager.switch_to("test_scene")

    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    scene_manager.handle_event(event)

    assert mock_scene.event_handled


def test_scene_update(scene_manager, mock_scene):
    """Test scene update."""
    scene_manager.add_scene("test_scene", mock_scene)
    scene_manager.switch_to("test_scene")

    scene_manager.update(0.016)  # Simulate 60 FPS
    assert mock_scene.updated


def test_scene_render(scene_manager, mock_scene):
    """Test scene rendering."""
    scene_manager.add_scene("test_scene", mock_scene)
    scene_manager.switch_to("test_scene")

    surface = pygame.Surface((800, 600))
    scene_manager.render(surface)
    assert mock_scene.rendered
