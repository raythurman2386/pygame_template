# src/entities/paddle.py
import pygame
from .entity import Entity


class Paddle(Entity):
    """Paddle entity for Pong game."""

    def __init__(self, x, y, width=20, height=100, speed=400, is_player=True):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.is_player = is_player
        self.move_up = False
        self.move_down = False
        self.score = 0

    def update(self, dt, ball=None):
        """Update paddle position."""
        if self.is_player:
            # Player paddle is controlled by input
            if self.move_up:
                self.y -= self.speed * dt
            if self.move_down:
                self.y += self.speed * dt
        else:
            # AI paddle tracks the ball
            if ball:
                # Simple AI: track the ball but with some limitations
                target_y = ball.y - self.height / 2

                # Add some constraints to make AI beatable
                if abs(self.y - target_y) > 10:  # Avoid jitter
                    if self.y < target_y:
                        # Don't move at full speed
                        self.y += min(self.speed * 0.7 * dt, target_y - self.y)
                    else:
                        self.y -= min(self.speed * 0.7 * dt, self.y - target_y)

        # Update collision rect
        super().update(dt)

    def render(self, surface):
        """Draw the paddle."""
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

    def increment_score(self):
        """Increase player's score."""
        self.score += 1
        return self.score
