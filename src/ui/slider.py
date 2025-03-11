import pygame
from .element import UIElement
from .label import Label


class Slider(UIElement):
    """Interactive slider control for numeric values."""

    def __init__(
        self, x, y, width, height, min_value=0.0, max_value=1.0, initial_value=0.5, label=None
    ):
        super().__init__(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        # Ensure initial_value is within min and max
        self.value = max(min_value, min(max_value, initial_value))
        self.dragging = False
        self.label_text = label

        # Colors
        self.bar_color = (80, 80, 80)
        self.handle_color = (200, 200, 200)
        self.handle_hover_color = (220, 220, 220)
        self.handle_active_color = (240, 240, 240)

        # Handle properties
        self.handle_width = 16
        self.handle_height = height
        self.handle_rect = pygame.Rect(
            self.get_handle_x_position(), y, self.handle_width, self.handle_height
        )

        # Create label if specified
        if label:
            self.label = Label(
                x=x,
                y=y - 20,  # Position above slider
                width=width,
                height=20,
                text=f"{label}: {self.value:.2f}",
            )
        else:
            self.label = None

    def set_font(self, font):
        """Set font for the label."""
        if self.label:
            self.label.set_font(font)

    def get_handle_x_position(self):
        """Calculate the handle's x position based on the current value."""
        value_range = self.max_value - self.min_value
        normalized_value = (self.value - self.min_value) / value_range
        return self.rect.x + int(normalized_value * (self.rect.width - self.handle_width))

    def update_value_from_handle_position(self):
        """Update the slider value based on handle position."""
        handle_offset = self.handle_rect.x - self.rect.x
        normalized_value = handle_offset / (self.rect.width - self.handle_width)
        self.value = self.min_value + normalized_value * (self.max_value - self.min_value)

        # Update label text if available
        if self.label:
            self.label.set_text(f"{self.label_text}: {self.value:.2f}")

    def handle_event(self, event):
        """Process mouse events."""
        if not self.enabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.handle_rect.collidepoint(event.pos):
                    self.dragging = True
                elif self.rect.collidepoint(event.pos):
                    # Jump to click position
                    self.handle_rect.x = max(
                        self.rect.x,
                        min(
                            event.pos[0] - self.handle_width // 2,
                            self.rect.x + self.rect.width - self.handle_width,
                        ),
                    )
                    self.update_value_from_handle_position()
                    self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_rect.x = max(
                    self.rect.x,
                    min(
                        event.pos[0] - self.handle_width // 2,
                        self.rect.x + self.rect.width - self.handle_width,
                    ),
                )
                self.update_value_from_handle_position()

    def update(self, dt):
        """Update slider state."""
        # Update handle position from value
        self.handle_rect.x = self.get_handle_x_position()

    def render(self, surface):
        """Draw the slider control."""
        if not self.visible:
            return

        # Draw slider bar
        bar_rect = pygame.Rect(
            self.rect.x, self.rect.y + (self.rect.height - 4) // 2, self.rect.width, 4
        )
        pygame.draw.rect(surface, self.bar_color, bar_rect)

        # Draw filled portion
        filled_width = self.handle_rect.x - self.rect.x + self.handle_width // 2
        filled_rect = pygame.Rect(self.rect.x, bar_rect.y, filled_width, bar_rect.height)
        pygame.draw.rect(surface, self.handle_color, filled_rect)

        # Draw handle
        pygame.draw.rect(
            surface,
            self.handle_active_color if self.dragging else self.handle_color,
            self.handle_rect,
        )

        # Draw label if available
        if self.label:
            self.label.render(surface)
