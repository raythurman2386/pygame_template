import pygame
from .scene_manager import SceneManager
from .resource_manager import ResourceManager
from ..utils.logger import GameLogger
from ..utils.performance import performance
import logging


class Engine:
    """Core game engine handling pygame initialization and main loop."""

    def __init__(self, width=800, height=600, title="PyGame Template", fps=60):
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.running = False
        self.clock = None
        self.screen = None

        # Initialize logger
        self.logger = GameLogger.get_logger("Engine")
        self.debug_logging = False

        # Initialize managers right away
        self.resource_manager = ResourceManager()
        self.scene_manager = SceneManager(self)
        self.settings = SimpleSettings()

    def initialize(self):
        """Set up pygame and initialize core systems."""
        pygame.init()
        pygame.mixer.init()

        # Set up display mode based on fullscreen setting
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.logger.info("Game engine initialized successfully")

    def toggle_debug_logging(self):
        """Toggle debug logging on/off."""
        self.debug_logging = not self.debug_logging
        new_level = logging.DEBUG if self.debug_logging else logging.INFO
        GameLogger.set_all_loggers_level(new_level)
        self.logger.info(f"Debug logging {'enabled' if self.debug_logging else 'disabled'}")

    def handle_events(self):
        """Process all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.logger.info("Quit event received")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.toggle_debug_logging()
                elif event.key == pygame.K_F2:
                    performance.toggle_metrics_display()
                    self.logger.debug("Performance metrics display toggled")

            self.scene_manager.handle_event(event)

    def update(self, dt):
        """Update game state."""
        performance.start_frame()

        performance.start_section("scene_update")
        self.scene_manager.update(dt)
        performance.end_section()

    def render(self):
        """Render current frame."""
        performance.start_section("render")
        self.screen.fill((0, 0, 0))  # Background color
        self.scene_manager.render(self.screen)

        # Draw performance metrics if enabled
        performance.draw_metrics(self.screen)

        pygame.display.flip()
        performance.end_section()

    def run(self):
        """Main game loop."""
        self.initialize()
        self.running = True
        self.logger.info("Starting main game loop")

        # Main game loop
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds

            performance.start_section("event_handling")
            self.handle_events()
            performance.end_section()

            self.update(dt)
            self.render()

        self.cleanup()

    def cleanup(self):
        """Clean up resources before exiting."""
        self.logger.info("Cleaning up and shutting down")
        pygame.quit()


class SimpleSettings:
    """Placeholder for game settings."""

    def __init__(self):
        self.music_enabled = True
        self.sfx_enabled = True
        self.music_volume = 0.5
        self.master_volume = 1.0
        self.fullscreen = False
        self.vsync = True
        self.difficulty = "normal"

    def save(self):
        """Stub for saving settings."""
        pass
