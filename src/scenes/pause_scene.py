# src/scenes/pause_scene.py
import pygame
from .scene import Scene
from src.ui import Button, Menu


class PauseMenuScene(Scene):
    """Overlay scene that pauses the game."""

    def __init__(self, engine):
        super().__init__(engine)
        self.previous_scene_name = None  # Store scene name instead of scene object
        self.overlay_surface = None
        self.menu_font = None
        self.pause_text = None
        self.menu = None

    def enter(self):
        """Set up the pause menu overlay."""
        # Store the current game state's name
        self.previous_scene_name = "game"  # Assume we're always pausing the game

        # Create semi-transparent overlay
        self.overlay_surface = pygame.Surface(
            (self.engine.width, self.engine.height), pygame.SRCALPHA
        )
        self.overlay_surface.fill((0, 0, 0, 128))  # Semi-transparent black

        # Create font
        self.menu_font = pygame.font.SysFont(None, 36)

        # Create pause text
        self.pause_text = self.menu_font.render("PAUSED", True, (255, 255, 255))

        # Create menu
        self.menu = Menu(
            x=self.engine.width // 2,
            y=self.engine.height // 2,
            width=250,
            height=300,
            centered=True,
        )
        self.menu.set_font(self.menu_font)

        # Add menu buttons
        self.menu.add_button("Resume", self.on_resume_clicked)
        self.menu.add_button("Options", self.on_options_clicked)
        self.menu.add_button("Main Menu", self.on_main_menu_clicked)

    def exit(self):
        """Clean up resources when leaving pause menu."""
        pass

    def handle_event(self, event):
        """Process events while paused."""
        self.menu.handle_event(event)

        # Allow ESC to unpause
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_resume_clicked()

    def update(self, dt):
        """Update menu animations."""
        self.menu.update(dt)

    def render(self, surface):
        """Draw the pause menu overlay."""
        # First render the game underneath
        game_scene = self.engine.scene_manager.scenes.get("game")
        if game_scene and game_scene != self:  # Prevent recursion
            # Take a snapshot of the game scene once
            game_scene.render(surface)

        # Draw semi-transparent overlay
        surface.blit(self.overlay_surface, (0, 0))

        # Draw pause text
        text_x = (self.engine.width - self.pause_text.get_width()) // 2
        surface.blit(self.pause_text, (text_x, 100))

        # Draw menu
        self.menu.render(surface)

    # Button event handlers
    def on_resume_clicked(self):
        """Resume the game."""
        # Return to the game scene
        self.engine.scene_manager.switch_to("game")

    def on_options_clicked(self):
        """Open options menu."""
        # We need to remember we're coming from pause menu
        self.engine.scene_manager.switch_to("options_from_pause")

    def on_main_menu_clicked(self):
        """Return to main menu."""
        self.engine.scene_manager.switch_to("main_menu")
