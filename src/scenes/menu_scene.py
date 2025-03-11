import pygame

from src.scenes.scene import Scene
from src.ui.menu import Menu


class MainMenuScene(Scene):
    """Main menu scene that serves as the entry point to the game."""

    def __init__(self, engine):
        super().__init__(engine)
        self.title_font = None
        self.menu_font = None
        self.title_text = None
        self.menu = None
        self.background = None
        self.sfx_hover = None
        self.sfx_select = None

    def enter(self):
        """Initialize resources when scene becomes active."""
        # Load resources
        res_mgr = self.engine.resource_manager
        self.title_font = pygame.font.SysFont("Arial", 64)
        self.menu_font = pygame.font.SysFont("Arial", 32)
        self.background = res_mgr.get_image("menu_background")
        self.sfx_hover = res_mgr.get_sound("menu_hover")
        self.sfx_select = res_mgr.get_sound("menu_select")

        # Create title text
        self.title_text = self.title_font.render("Pygame Template", True, (255, 255, 255))

        # Create menu
        self.menu = Menu(
            x=self.engine.width // 2,
            y=self.engine.height // 2,
            width=300,
            height=400,
            centered=True,
        )

        # Add menu buttons
        self.menu.add_button("Play", self.on_play_clicked)
        self.menu.add_button("Options", self.on_options_clicked)
        self.menu.add_button("Credits", self.on_credits_clicked)
        self.menu.add_button("Quit", self.on_quit_clicked)

        # Set up event handlers
        self.menu.on_hover = self.on_button_hover

        # Start background music if available
        menu_music = res_mgr.get_sound("menu_music")
        if menu_music and self.engine.settings.music_enabled:
            pygame.mixer.music.load(menu_music)
            pygame.mixer.music.set_volume(self.engine.settings.music_volume)
            pygame.mixer.music.play(-1)  # Loop indefinitely

    def exit(self):
        """Clean up resources when leaving this scene."""
        # Stop music when leaving menu
        pygame.mixer.music.fadeout(500)  # Fade out over 500ms

    def handle_event(self, event):
        """Process incoming events."""
        self.menu.handle_event(event)

        # Add any additional input handling here

    def update(self, dt):
        """Update menu animations and effects."""
        self.menu.update(dt)

        # Add any animations or effects here

    def render(self, surface):
        """Draw the menu to the screen."""
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            # If no background image, use a gradient
            self.draw_gradient_background(surface)

        # Draw title
        title_x = (self.engine.width - self.title_text.get_width()) // 2
        surface.blit(self.title_text, (title_x, 100))

        # Draw menu
        self.menu.render(surface)

    def draw_gradient_background(self, surface):
        """Draw a nice gradient background."""
        height = self.engine.height
        for y in range(height):
            # Create gradient from dark blue to lighter blue
            color = (0, 0, 50 + int(y * 0.15))
            pygame.draw.line(surface, color, (0, y), (self.engine.width, y))

    def on_button_hover(self, button):
        """Handle button hover events."""
        if self.sfx_hover and self.engine.settings.sfx_enabled:
            self.sfx_hover.play()

    def on_play_clicked(self):
        """Start the game."""
        if self.sfx_select and self.engine.settings.sfx_enabled:
            self.sfx_select.play()
        self.engine.scene_manager.switch_to("game")

    def on_options_clicked(self):
        """Open options menu."""
        if self.sfx_select and self.engine.settings.sfx_enabled:
            self.sfx_select.play()
        self.engine.scene_manager.switch_to("options")

    def on_credits_clicked(self):
        """Show credits screen."""
        if self.sfx_select and self.engine.settings.sfx_enabled:
            self.sfx_select.play()
        self.engine.scene_manager.switch_to("credits")

    def on_quit_clicked(self):
        """Exit the game."""
        if self.sfx_select and self.engine.settings.sfx_enabled:
            self.sfx_select.play()
        # Add a small delay so the sound plays before quitting
        pygame.time.delay(200)
        self.engine.running = False
