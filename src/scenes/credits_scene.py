import pygame
from .scene import Scene
from src.ui import Button, Label, Menu


class CreditsScene(Scene):
    """Scene that displays game credits."""

    def __init__(self, engine):
        super().__init__(engine)
        self.title_font = None
        self.content_font = None
        self.title_text = None
        self.credits_menu = None
        self.background = None

    def enter(self):
        """Initialize credits screen."""
        self.title_font = pygame.font.SysFont(None, 64)
        self.content_font = pygame.font.SysFont(None, 28)

        # Create title text
        self.title_text = self.title_font.render("Credits", True, (255, 255, 255))

        # Create menu for credits content and back button
        self.credits_menu = Menu(
            x=self.engine.width // 2, y=160, width=500, height=400, centered=True
        )
        self.credits_menu.set_font(self.content_font)

        self.credits_menu.add_label("Programming")
        self.credits_menu.add_label("Your Team Members")
        self.credits_menu.add_spacer(10)

        self.credits_menu.add_label("Art & Sound")
        self.credits_menu.add_label("Your Artists")
        self.credits_menu.add_spacer(10)

        self.credits_menu.add_label("Special Thanks")
        self.credits_menu.add_label("PyGame Community")
        self.credits_menu.add_spacer(10)

        # Add back button
        self.credits_menu.add_button("Back to Main Menu", self.on_back_clicked)

        print("Credits scene setup complete")

    def exit(self):
        """Clean up when leaving credits screen."""
        print("==== EXITING CREDITS SCENE ====")

    def handle_event(self, event):
        """Process events."""
        self.credits_menu.handle_event(event)

        # Allow ESC to return to main menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_back_clicked()

    def update(self, dt):
        """Update credits animations."""
        self.credits_menu.update(dt)

    def render(self, surface):
        """Draw the credits screen."""
        # Draw background gradient
        self.draw_gradient_background(surface)

        # Draw title
        title_x = (self.engine.width - self.title_text.get_width()) // 2
        surface.blit(self.title_text, (title_x, 50))

        # Draw credits content
        self.credits_menu.render(surface)

    def draw_gradient_background(self, surface):
        """Draw a nice gradient background."""
        height = self.engine.height
        for y in range(height):
            # Create gradient from dark blue to black
            color_val = max(0, int(50 - (y / height) * 50))
            color = (0, 0, color_val)
            pygame.draw.line(surface, color, (0, y), (self.engine.width, y))

    def on_back_clicked(self):
        """Return to main menu."""
        print("Back button clicked, returning to main menu")
        self.engine.scene_manager.switch_to("main_menu")
