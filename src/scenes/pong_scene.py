# src/scenes/pong_scene.py
import pygame
from .scene import Scene
from src.objects.paddle import Paddle
from src.objects.ball import Ball
from src.ui import Label


class PongScene(Scene):
    """Simple Pong game implementation."""

    def __init__(self, engine):
        super().__init__(engine)
        self.ball = None
        self.player_paddle = None
        self.ai_paddle = None
        self.score_font = None
        self.player_score_label = None
        self.ai_score_label = None
        self.paused = False
        self.game_over = False
        self.max_score = 5  # First to reach this score wins

    def enter(self):
        """Initialize pong game."""
        # Get window dimensions for positioning
        width = self.engine.width
        height = self.engine.height

        # Create paddles
        paddle_width = 20
        paddle_height = 100
        paddle_offset = 50

        self.player_paddle = Paddle(
            x=paddle_offset,
            y=(height - paddle_height) // 2,
            width=paddle_width,
            height=paddle_height,
            is_player=True,
        )

        self.ai_paddle = Paddle(
            x=width - paddle_offset - paddle_width,
            y=(height - paddle_height) // 2,
            width=paddle_width,
            height=paddle_height,
            is_player=False,
        )

        # Create ball
        self.ball = Ball(x=width // 2, y=height // 2, size=15, speed=300)

        # Set up score display
        res_mgr = self.engine.resource_manager
        self.score_font = pygame.font.SysFont(None, 64)

        self.player_score_label = Label(
            x=width // 4, y=50, width=100, height=80, text="0", centered=True
        )
        self.player_score_label.set_font(self.score_font)

        self.ai_score_label = Label(
            x=width - width // 4, y=50, width=100, height=80, text="0", centered=True
        )
        self.ai_score_label.set_font(self.score_font)

        # Reset game state
        self.paused = False
        self.game_over = False

        # Play game music if available
        game_music = res_mgr.get_sound("game_music")
        if game_music and self.engine.settings.music_enabled:
            pygame.mixer.music.load(game_music)
            pygame.mixer.music.set_volume(self.engine.settings.music_volume)
            pygame.mixer.music.play(-1)  # Loop indefinitely

    def exit(self):
        """Clean up resources when leaving the game."""
        # Stop music when leaving
        pygame.mixer.music.fadeout(500)

    def handle_event(self, event):
        """Process game events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Pause the game
                self.engine.scene_manager.switch_to("pause")

            # Player paddle controls
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player_paddle.move_up = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.player_paddle.move_down = True

        elif event.type == pygame.KEYUP:
            # Player paddle controls
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player_paddle.move_up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.player_paddle.move_down = False

    def update(self, dt):
        """Update game state."""
        if self.paused or self.game_over:
            return

        # Update entities
        self.player_paddle.update(dt)
        self.ai_paddle.update(dt, self.ball)
        self.ball.update(dt)

        # Check for collisions
        self.check_collisions()

        # Check for scoring
        self.check_scoring()

        # Check for game over
        if self.player_paddle.score >= self.max_score or self.ai_paddle.score >= self.max_score:
            self.game_over = True
            # Determine winner and go to game over screen
            player_won = self.player_paddle.score >= self.max_score
            # Pass score and win state to game over scene
            game_over_scene = self.engine.scene_manager.scenes.get("game_over")
            if game_over_scene:
                final_score = max(self.player_paddle.score, self.ai_paddle.score)
                self.engine.scene_manager.switch_to("game_over")
                game_over_scene.enter(final_score=final_score, win_state=player_won)

    def check_collisions(self):
        """Handle collisions between ball and objects."""
        height = self.engine.height

        # Ball collision with top and bottom walls
        if self.ball.y <= 0 or self.ball.y + self.ball.height >= height:
            self.ball.bounce_vertical()

            # Keep ball in bounds
            if self.ball.y <= 0:
                self.ball.y = 0
            elif self.ball.y + self.ball.height >= height:
                self.ball.y = height - self.ball.height

        # Ball collision with paddles
        if self.ball.rect.colliderect(self.player_paddle.rect) or self.ball.rect.colliderect(
            self.ai_paddle.rect
        ):
            self.ball.bounce_horizontal()

            # Play sound effect
            bounce_sfx = self.engine.resource_manager.get_sound("paddle_hit")
            if bounce_sfx and self.engine.settings.sfx_enabled:
                bounce_sfx.play()

            # Add a little y velocity based on where the ball hit the paddle
            if self.ball.rect.colliderect(self.player_paddle.rect):
                relative_intersect_y = (
                    self.player_paddle.rect.y + (self.player_paddle.rect.height / 2)
                ) - self.ball.rect.centery
                normalized_relative_intersect_y = relative_intersect_y / (
                    self.player_paddle.rect.height / 2
                )
                self.ball.dy = -normalized_relative_intersect_y * (abs(self.ball.dx) * 0.75)

            elif self.ball.rect.colliderect(self.ai_paddle.rect):
                relative_intersect_y = (
                    self.ai_paddle.rect.y + (self.ai_paddle.rect.height / 2)
                ) - self.ball.rect.centery
                normalized_relative_intersect_y = relative_intersect_y / (
                    self.ai_paddle.rect.height / 2
                )
                self.ball.dy = -normalized_relative_intersect_y * (abs(self.ball.dx) * 0.75)

        # Constrain paddles to screen
        if self.player_paddle.y < 0:
            self.player_paddle.y = 0
        elif self.player_paddle.y + self.player_paddle.height > height:
            self.player_paddle.y = height - self.player_paddle.height

        if self.ai_paddle.y < 0:
            self.ai_paddle.y = 0
        elif self.ai_paddle.y + self.ai_paddle.height > height:
            self.ai_paddle.y = height - self.ai_paddle.height

    def check_scoring(self):
        """Check if a player scored and update accordingly."""
        width = self.engine.width

        # Ball goes past left edge (AI scores)
        if self.ball.x + self.ball.width < 0:
            self.ai_paddle.increment_score()
            self.ai_score_label.set_text(str(self.ai_paddle.score))
            self.ball.x = width // 2
            self.ball.y = self.engine.height // 2
            self.ball.reset()

            # Play sound effect
            score_sfx = self.engine.resource_manager.get_sound("score")
            if score_sfx and self.engine.settings.sfx_enabled:
                score_sfx.play()

        # Ball goes past right edge (player scores)
        elif self.ball.x > width:
            self.player_paddle.increment_score()
            self.player_score_label.set_text(str(self.player_paddle.score))
            self.ball.x = width // 2
            self.ball.y = self.engine.height // 2
            self.ball.reset()

            # Play sound effect
            score_sfx = self.engine.resource_manager.get_sound("score")
            if score_sfx and self.engine.settings.sfx_enabled:
                score_sfx.play()

    def render(self, surface):
        """Draw the game scene."""
        # Fill background
        surface.fill((0, 0, 0))

        # Draw center line
        center_x = self.engine.width // 2
        pygame.draw.line(
            surface,
            (255, 255, 255, 128),  # Semi-transparent white
            (center_x, 0),
            (center_x, self.engine.height),
            3,
        )

        # Draw circle in the middle
        pygame.draw.circle(
            surface,
            (255, 255, 255, 128),  # Semi-transparent white
            (center_x, self.engine.height // 2),
            50,
            3,
        )

        # Draw score labels
        self.player_score_label.render(surface)
        self.ai_score_label.render(surface)

        # Draw game entities
        self.player_paddle.render(surface)
        self.ai_paddle.render(surface)
        self.ball.render(surface)
