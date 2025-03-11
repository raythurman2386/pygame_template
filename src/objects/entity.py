import pygame


class Entity:
    """Base class for all game objects."""

    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True

    def update(self, dt):
        """Update entity state."""
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self, surface):
        """Render entity to the given surface."""
        pass

    def get_position(self):
        """Get current position as a tuple."""
        return (self.x, self.y)

    def set_position(self, x, y):
        """Set position."""
        self.x = x
        self.y = y

    def get_rect(self):
        """Get the collision rectangle."""
        return self.rect
