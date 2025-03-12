import pygame
from .scene_manager import SceneManager
from .resource_manager import ResourceManager
from ..utils.logger import GameLogger
from ..utils.performance import performance
from config.settings import Settings
from config.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
import logging


class Engine:
    """Core game engine handling pygame initialization and main loop."""

    def __init__(
        self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title="PyGame Pong Template", fps=60
    ):
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.running = False
        self.clock = None
        self.screen = None

        # Store original window dimensions for proper fullscreen handling
        self.original_width = width
        self.original_height = height

        # Initialize logger
        self.logger = GameLogger.get_logger("Engine")
        self.debug_logging = False

        # Initialize managers right away
        self.resource_manager = ResourceManager()
        self.scene_manager = SceneManager(self)
        self.settings = Settings()

    def initialize(self):
        """Set up pygame and initialize core systems."""
        pygame.init()
        pygame.mixer.init()

        # Set up display mode based on fullscreen setting
        if self.settings.fullscreen:
            # Get current display info for proper fullscreen resolution
            display_info = pygame.display.Info()
            self.width = display_info.current_w
            self.height = display_info.current_h

            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
            self.logger.info(f"Initialized in fullscreen mode: {self.width}x{self.height}")
        else:
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF
            )
            self.logger.info(f"Initialized in windowed mode: {self.width}x{self.height}")

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
                elif event.key == pygame.K_ESCAPE:
                    if (
                        "pause" in self.settings.key_bindings
                        and event.key == self.settings.key_bindings["pause"]
                    ):
                        self.logger.debug("Pause key pressed")

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
        self.screen.fill(BLACK)
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
            dt = (
                self.clock.tick(self.settings.fps_limit) / 1000.0
            )  # Delta time in seconds using fps from settings

            performance.start_section("event_handling")
            self.handle_events()
            performance.end_section()

            self.update(dt)
            self.render()

        self.cleanup()

    def cleanup(self):
        """Clean up resources before exiting."""
        self.logger.info("Cleaning up and shutting down")

        # If in fullscreen mode, switch back to windowed mode first
        # This helps prevent display issues when exiting the game
        if self.settings.fullscreen:
            self.logger.info("Exiting fullscreen mode before shutdown")
            try:
                # Restore original window size
                pygame.display.set_mode(
                    (self.original_width, self.original_height), pygame.HWSURFACE | pygame.DOUBLEBUF
                )
                # Small delay to allow display to settle
                pygame.time.delay(100)
            except Exception as e:
                self.logger.error(f"Error when exiting fullscreen: {e}")

        # Save settings before exiting
        self.settings.save()
        pygame.quit()
