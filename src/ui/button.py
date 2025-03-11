import pygame
from .element import UIElement


class Button(UIElement):
    """Interactive button UI element."""

    def __init__(self, x, y, width, height, text="", callback=None, centered=False):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.centered = centered
        self.font = None
        self.text_surface = None
        self.hover = False
        self.pressed = False

        # Colors
        self.bg_color = (80, 80, 80)
        self.hover_color = (100, 100, 100)
        self.pressed_color = (60, 60, 60)
        self.text_color = (255, 255, 255)
        self.border_color = (120, 120, 120)
        self.disabled_color = (60, 60, 60)
        self.disabled_text_color = (160, 160, 160)

        # Center the button if needed
        if centered:
            self.rect.x -= self.rect.width // 2
            self.rect.y -= self.rect.height // 2

    def set_font(self, font):
        """Set button font."""
        self.font = font
        self.update_text_surface()

    def set_text(self, text):
        """Change the button text."""
        self.text = text
        self.update_text_surface()

    def set_callback(self, callback):
        """Change the button callback function."""
        self.callback = callback

    def update_text_surface(self):
        """Update the rendered text surface."""
        if self.font:
            color = self.disabled_text_color if not self.enabled else self.text_color
            self.text_surface = self.font.render(self.text, True, color)

    def handle_event(self, event):
        """Process mouse events for this button."""
        if not self.enabled or not self.visible:
            return

        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is over button
            self.hover = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hover:  # Left mouse button
                self.pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:  # Left mouse button
                self.pressed = False
                if self.hover and self.callback:
                    self.callback()

    def update(self, dt):
        """Update button state."""
        pass

    def render(self, surface):
        """Draw the button."""
        if not self.visible:
            return

        # Choose color based on state
        if not self.enabled:
            bg_color = self.disabled_color
        elif self.pressed:
            bg_color = self.pressed_color
        elif self.hover:
            bg_color = self.hover_color
        else:
            bg_color = self.bg_color

        # Draw button background with rounded corners
        pygame.draw.rect(surface, bg_color, self.rect, 0, 5)

        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 2, 5)

        # Create text surface if it doesn't exist
        if not self.text_surface and self.text:
            self.update_text_surface()

        # Draw text if available
        if self.text_surface:
            text_x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
            text_y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
            surface.blit(self.text_surface, (text_x, text_y))
        else:
            # Fallback - draw text directly if surface not available
            if self.text and not self.text_surface:
                fallback_font = pygame.font.SysFont(None, 24)
                fallback_text = fallback_font.render(self.text, True, self.text_color)
                text_x = self.rect.x + (self.rect.width - fallback_text.get_width()) // 2
                text_y = self.rect.y + (self.rect.height - fallback_text.get_height()) // 2
                surface.blit(fallback_text, (text_x, text_y))
