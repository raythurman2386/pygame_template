"""Test suite for the performance monitor."""

import time
import pytest
import pygame
from src.utils.performance import PerformanceMonitor


@pytest.fixture
def performance_monitor():
    """Create a performance monitor instance for testing."""
    monitor = PerformanceMonitor()
    monitor.clear()  # Ensure clean state
    return monitor


def test_performance_monitor_singleton():
    """Test performance monitor singleton pattern."""
    monitor1 = PerformanceMonitor()
    monitor2 = PerformanceMonitor()
    assert monitor1 is monitor2


def test_frame_timing(performance_monitor):
    """Test frame timing functionality."""
    performance_monitor.start_frame()
    time.sleep(0.001)  # Small delay to ensure measurable time difference
    performance_monitor.start_frame()

    assert len(performance_monitor.frame_times) == 2
    assert performance_monitor.frame_times[-1] > performance_monitor.frame_times[-2]


def test_section_timing(performance_monitor):
    """Test section timing functionality."""
    performance_monitor.start_section("test_section")
    time.sleep(0.001)  # Small delay to ensure measurable time
    performance_monitor.end_section()

    stats = performance_monitor.get_section_stats("test_section")
    assert stats["min"] > 0
    assert stats["max"] > 0
    assert stats["avg"] > 0


def test_fps_calculation(performance_monitor):
    """Test FPS calculation."""
    # Simulate a few frames with controlled timing
    for _ in range(3):
        performance_monitor.start_frame()
        time.sleep(0.001)  # Small controlled delay

    fps = performance_monitor.get_fps()
    assert fps > 0  # We should get some FPS value


def test_metrics_display_toggle(performance_monitor):
    """Test toggling metrics display."""
    initial_state = performance_monitor.show_metrics
    performance_monitor.toggle_metrics_display()
    assert performance_monitor.show_metrics != initial_state
    performance_monitor.toggle_metrics_display()
    assert performance_monitor.show_metrics == initial_state


def test_section_stats_empty(performance_monitor):
    """Test getting stats for non-existent section."""
    stats = performance_monitor.get_section_stats("nonexistent")
    assert stats["min"] == 0.0
    assert stats["max"] == 0.0
    assert stats["avg"] == 0.0


def test_multiple_sections(performance_monitor):
    """Test timing multiple sections."""
    sections = ["section1", "section2", "section3"]

    for section in sections:
        performance_monitor.start_section(section)
        time.sleep(0.001)  # Small controlled delay
        performance_monitor.end_section()

    for section in sections:
        stats = performance_monitor.get_section_stats(section)
        assert stats["min"] > 0
        assert stats["max"] > 0
        assert stats["avg"] > 0


def test_clear_performance_data(performance_monitor):
    """Test clearing performance data."""
    performance_monitor.start_frame()
    performance_monitor.start_section("test")
    performance_monitor.end_section()

    performance_monitor.clear()

    assert len(performance_monitor.frame_times) == 0
    assert len(performance_monitor.section_times) == 0


def test_draw_metrics(performance_monitor):
    """Test drawing metrics to surface."""
    surface = pygame.Surface((800, 600))

    # Test with metrics disabled
    performance_monitor.show_metrics = False
    performance_monitor.draw_metrics(surface)

    # Test with metrics enabled
    performance_monitor.show_metrics = True
    performance_monitor.start_frame()
    performance_monitor.start_section("test")
    time.sleep(0.001)  # Add some measurable time
    performance_monitor.end_section()
    performance_monitor.draw_metrics(surface)

    # If we got here without exceptions, test passes
    assert True


def test_max_frame_samples(performance_monitor):
    """Test that frame samples are limited to max_frame_samples."""
    # Add more frames than the limit
    for _ in range(performance_monitor.max_frame_samples + 10):
        performance_monitor.start_frame()

    assert len(performance_monitor.frame_times) <= performance_monitor.max_frame_samples
