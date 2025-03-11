# src/entities/ball.py
import pygame
import random
from .entity import Entity


class Ball(Entity):
    """Ball entity for Pong game."""

    def __init__(self, x, y, size=15, speed=300):
        super().__init__(x, y, size, size)
        self.size = size
        self.base_speed = speed
        self.speed = speed
        self.dx = 0
        self.dy = 0
        self.reset()

    def reset(self):
        """Reset ball to center with random direction."""
        # Start with random angle but avoid too horizontal angles
        angle = random.uniform(0.5, 1.0) * random.choice([-1, 1])
        self.dx = self.base_speed * (1.0 if random.random() > 0.5 else -1.0)
        self.dy = self.base_speed * angle

        # Normalize to maintain consistent speed
        length = (self.dx**2 + self.dy**2) ** 0.5
        self.dx = self.dx / length * self.base_speed
        self.dy = self.dy / length * self.base_speed

        # Reset speed
        self.speed = self.base_speed

    def update(self, dt):
        """Update ball position."""
        self.x += self.dx * dt
        self.y += self.dy * dt

        # Update the collision rect
        super().update(dt)

    def render(self, surface):
        """Draw the ball."""
        pygame.draw.circle(surface, (255, 255, 255), self.rect.center, self.size // 2)

    def bounce_horizontal(self):
        """Reverse horizontal direction."""
        self.dx *= -1

        # Increase speed slightly with each bounce
        self.dx *= 1.05
        self.dy *= 1.05

    def bounce_vertical(self):
        """Reverse vertical direction."""
        self.dy *= -1
