# src/scenes/options_scene.py
import pygame
from .scene import Scene
from src.ui import Button, Label, Menu, ToggleButton


class OptionsMenuScene(Scene):
    """Simplified menu for adjusting game settings."""

    def __init__(self, engine, return_scene="main_menu"):
        super().__init__(engine)
        self.return_scene = return_scene  # Where to return after options
        self.title_font = None
        self.menu_font = None
        self.title_text = None
        self.options_menu = None

        # UI controls for settings
        self.fullscreen_toggle = None
        self.music_toggle = None
        self.sfx_toggle = None

    def enter(self):
        """Initialize options menu."""
        print("==== ENTERING OPTIONS SCENE ====")

        # Create fonts
        self.title_font = pygame.font.SysFont(None, 48)
        self.menu_font = pygame.font.SysFont(None, 32)

        # Create title text
        self.title_text = self.title_font.render("Options", True, (255, 255, 255))

        # Create options menu
        self.options_menu = Menu(
            x=self.engine.width // 2, y=150, width=400, height=350, centered=True
        )
        self.options_menu.set_font(self.menu_font)

        # Add section header
        header = Label(0, 0, 350, 40, "Game Settings", centered=True)
        header.set_font(self.menu_font)
        header.set_background_color((40, 40, 80))
        self.options_menu.add_element(header)

        # Add spacer
        self.options_menu.add_spacer(20)

        # Fullscreen toggle
        self.fullscreen_toggle = ToggleButton(
            x=0,
            y=0,  # Will be positioned by menu
            width=350,
            height=40,
            label="Fullscreen",
            is_on=self.engine.settings.fullscreen,
        )
        self.options_menu.add_element(self.fullscreen_toggle)

        # Music toggle
        self.music_toggle = ToggleButton(
            x=0,
            y=0,  # Will be positioned by menu
            width=350,
            height=40,
            label="Music",
            is_on=self.engine.settings.music_enabled,
        )
        self.options_menu.add_element(self.music_toggle)

        # Sound effects toggle
        self.sfx_toggle = ToggleButton(
            x=0,
            y=0,  # Will be positioned by menu
            width=350,
            height=40,
            label="Sound Effects",
            is_on=self.engine.settings.sfx_enabled,
        )
        self.options_menu.add_element(self.sfx_toggle)

        # Add spacer
        self.options_menu.add_spacer(30)

        # Add buttons at the bottom
        self.options_menu.add_button("Apply", self.on_apply_clicked)
        self.options_menu.add_button("Back", self.on_back_clicked)

        print("Options scene setup complete")

    def exit(self):
        """Clean up when leaving options menu."""
        print("==== EXITING OPTIONS SCENE ====")

    def handle_event(self, event):
        """Process events."""
        self.options_menu.handle_event(event)

        # Allow ESC to return without saving
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_back_clicked()

    def update(self, dt):
        """Update menu animations."""
        self.options_menu.update(dt)

    def render(self, surface):
        """Draw the options menu."""
        # Fill background
        surface.fill((20, 20, 40))

        # Draw title
        title_x = (self.engine.width - self.title_text.get_width()) // 2
        surface.blit(self.title_text, (title_x, 70))

        # Draw options menu
        self.options_menu.render(surface)

    def on_apply_clicked(self):
        """Apply and save settings."""
        print("Apply button clicked, saving settings")

        # Update settings from UI controls
        settings = self.engine.settings

        # Check if fullscreen changed
        fullscreen_changed = settings.fullscreen != self.fullscreen_toggle.is_on

        # Update settings
        settings.fullscreen = self.fullscreen_toggle.is_on
        settings.music_enabled = self.music_toggle.is_on
        settings.sfx_enabled = self.sfx_toggle.is_on

        # Apply fullscreen setting if changed
        if fullscreen_changed:
            if settings.fullscreen:
                print("Switching to fullscreen mode")
                pygame.display.set_mode((self.engine.width, self.engine.height), pygame.FULLSCREEN)
            else:
                print("Switching to windowed mode")
                pygame.display.set_mode((self.engine.width, self.engine.height))

        # Apply audio settings
        if not settings.music_enabled:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        # Save settings
        settings.save()

        # Return to previous scene
        self.engine.scene_manager.switch_to(self.return_scene)

    def on_back_clicked(self):
        """Return without saving."""
        print("Back button clicked, returning without saving")
        self.engine.scene_manager.switch_to(self.return_scene)
