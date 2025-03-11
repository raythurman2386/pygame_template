import pygame
from .scene_manager import SceneManager
from .resource_manager import ResourceManager


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

    def handle_events(self):
        """Process all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.scene_manager.handle_event(event)

    def update(self, dt):
        """Update game state."""
        self.scene_manager.update(dt)

    def render(self):
        """Render current frame."""
        self.screen.fill((0, 0, 0))  # Background color
        self.scene_manager.render(self.screen)
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        self.initialize()
        self.running = True

        # Main game loop
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds
            self.handle_events()
            self.update(dt)
            self.render()

        self.cleanup()

    def cleanup(self):
        """Clean up resources before exiting."""
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
