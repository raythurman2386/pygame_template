import pygame


class UIElement:
    """Base class for all UI elements."""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True

    def handle_event(self, event):
        """Process pygame events."""
        pass

    def update(self, dt):
        """Update element state."""
        pass

    def render(self, surface):
        """Draw element to the surface."""
        pass

    def set_position(self, x, y):
        """Set the position of this element."""
        self.rect.x = x
        self.rect.y = y

    def set_size(self, width, height):
        """Set the size of this element."""
        self.rect.width = width
        self.rect.height = height

    def show(self):
        """Make this element visible."""
        self.visible = True

    def hide(self):
        """Make this element invisible."""
        self.visible = False

    def enable(self):
        """Enable this element."""
        self.enabled = True

    def disable(self):
        """Disable this element."""
        self.enabled = False
