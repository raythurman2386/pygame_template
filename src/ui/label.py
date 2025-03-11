import pygame
from .element import UIElement


class Label(UIElement):
    """Text display UI element."""

    def __init__(self, x, y, width, height, text="", centered=False):
        super().__init__(x, y, width, height)
        self.text = text
        self.centered = centered
        self.font = None
        self.text_surface = None
        self.text_color = (255, 255, 255)
        self.background_color = None  # Transparent by default
        self.padding = 5

        # Center the label if requested
        if centered:
            self.rect.x -= self.rect.width // 2
            self.rect.y -= self.rect.height // 2

    def set_font(self, font):
        """Set the font for this label."""
        self.font = font
        self.update_text_surface()

    def set_text(self, text):
        """Change the label text."""
        self.text = text
        self.update_text_surface()

    def set_text_color(self, color):
        """Set the text color."""
        self.text_color = color
        self.update_text_surface()

    def set_background_color(self, color):
        """Set the background color."""
        self.background_color = color

    def update_text_surface(self):
        """Render the text with the current font."""
        if self.font:
            self.text_surface = self.font.render(self.text, True, self.text_color)

    def handle_event(self, event):
        """Labels don't process events."""
        pass

    def update(self, dt):
        """Labels typically don't need updates."""
        pass

    def render(self, surface):
        """Draw the label to the surface."""
        if not self.visible:
            return

        # Draw background if specified
        if self.background_color:
            if len(self.background_color) == 4:  # RGBA color with alpha
                bg_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                bg_surface.fill(self.background_color)
                surface.blit(bg_surface, self.rect)
            else:  # RGB color without alpha
                pygame.draw.rect(surface, self.background_color, self.rect)

        # Draw text if available
        if self.text_surface:
            if self.centered:
                text_x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
                text_y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
            else:
                text_x = self.rect.x + self.padding
                text_y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2

            surface.blit(self.text_surface, (text_x, text_y))
