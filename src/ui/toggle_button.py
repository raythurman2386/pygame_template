import pygame
from .element import UIElement


class ToggleButton(UIElement):
    """A button that can be toggled on or off."""

    def __init__(self, x, y, width, height, label="Toggle", is_on=False):
        super().__init__(x, y, width, height)
        self.label_text = label
        self.is_on = is_on
        self.hover = False
        self.font = None
        self.label_surface = None

        # Toggle appearance
        self.toggle_width = 50
        self.toggle_height = 24

        # Colors
        self.off_color = (80, 80, 80)
        self.on_color = (0, 180, 0)
        self.hover_off_color = (100, 100, 100)
        self.hover_on_color = (0, 200, 0)
        self.text_color = (255, 255, 255)

    def set_font(self, font):
        """Set font for the label."""
        self.font = font
        self.update_label_surface()

    def update_label_surface(self):
        """Update the rendered label text."""
        if self.font and self.label_text:
            self.label_surface = self.font.render(self.label_text, True, self.text_color)

    def toggle(self):
        """Toggle the button state."""
        self.is_on = not self.is_on

    def set_state(self, is_on):
        """Set the toggle state directly."""
        self.is_on = is_on

    def handle_event(self, event):
        """Process mouse events."""
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # Left mouse button
                self.toggle()

    def update(self, dt):
        """Update toggle state."""
        pass

    def render(self, surface):
        """Draw the toggle button."""
        if not self.visible:
            return

        # Draw label
        if self.label_surface:
            label_x = self.rect.x + 10  # Left margin
            label_y = self.rect.y + (self.rect.height - self.label_surface.get_height()) // 2
            surface.blit(self.label_surface, (label_x, label_y))

        # Calculate toggle position (right side of the button)
        toggle_x = self.rect.x + self.rect.width - self.toggle_width - 10
        toggle_y = self.rect.y + (self.rect.height - self.toggle_height) // 2
        toggle_rect = pygame.Rect(toggle_x, toggle_y, self.toggle_width, self.toggle_height)

        # Choose toggle color based on state
        if self.is_on:
            toggle_color = self.hover_on_color if self.hover else self.on_color
        else:
            toggle_color = self.hover_off_color if self.hover else self.off_color

        # Draw toggle background (rounded rectangle)
        pygame.draw.rect(
            surface, toggle_color, toggle_rect, 0, self.toggle_height // 2  # Rounded corners
        )

        # Draw toggle knob
        knob_radius = self.toggle_height // 2 - 2
        if self.is_on:
            knob_x = toggle_x + self.toggle_width - knob_radius - 4
        else:
            knob_x = toggle_x + knob_radius + 4

        knob_y = toggle_y + self.toggle_height // 2
        pygame.draw.circle(surface, (255, 255, 255), (knob_x, knob_y), knob_radius)  # White knob
