import random

import pygame

from src.scenes.scene import Scene
from src.ui.menu import Menu


class GameOverScene(Scene):
    """Scene displayed when the game ends."""

    def __init__(self, engine):
        super().__init__(engine)
        self.title_font = None
        self.menu_font = None
        self.score_font = None
        self.title_text = None
        self.score_text = None
        self.menu = None
        self.background = None
        self.sfx_game_over = None
        self.sfx_hover = None
        self.sfx_select = None

        # Game results data
        self.final_score = 0
        self.win_state = False  # True if player won, False if lost

    def enter(self, final_score=0, win_state=False):
        """Initialize game over screen with results."""
        # Store game results
        self.final_score = final_score
        self.win_state = win_state

        # Load resources
        res_mgr = self.engine.resource_manager
        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 32)
        self.score_font = pygame.font.SysFont(None, 48)
        self.background = res_mgr.get_image("game_over_background")
        self.sfx_game_over = res_mgr.get_sound("game_over")
        self.sfx_hover = res_mgr.get_sound("menu_hover")
        self.sfx_select = res_mgr.get_sound("menu_select")

        # Create title text
        if self.win_state:
            self.title_text = self.title_font.render("Victory!", True, (255, 215, 0))
        else:
            self.title_text = self.title_font.render("Game Over", True, (255, 0, 0))

        # Create score text
        self.score_text = self.score_font.render(
            f"Score: {self.final_score}", True, (255, 255, 255)
        )

        # Create menu
        self.menu = Menu(
            x=self.engine.width // 2,
            y=self.engine.height // 2 + 50,
            width=300,
            height=200,
            centered=True,
        )

        # Add menu buttons
        self.menu.add_button("Play Again", self.on_play_again_clicked)
        self.menu.add_button("Main Menu", self.on_main_menu_clicked)

        # Set up event handlers
        self.menu.on_hover = self.on_button_hover

        # Play game over sound
        if self.sfx_game_over and self.engine.settings.sfx_enabled:
            self.sfx_game_over.play()

        # Start appropriate music if available
        if self.win_state:
            win_music = res_mgr.get_sound("victory_music")
            if win_music and self.engine.settings.music_enabled:
                pygame.mixer.music.load(win_music)
                pygame.mixer.music.set_volume(self.engine.settings.music_volume)
                pygame.mixer.music.play(-1)
        else:
            lose_music = res_mgr.get_sound("defeat_music")
            if lose_music and self.engine.settings.music_enabled:
                pygame.mixer.music.load(lose_music)
                pygame.mixer.music.set_volume(self.engine.settings.music_volume)
                pygame.mixer.music.play(-1)

    def exit(self):
        """Clean up resources before leaving."""
        pygame.mixer.music.fadeout(500)

    def handle_event(self, event):
        """Process events."""
        self.menu.handle_event(event)

    def update(self, dt):
        """Update animations and effects."""
        self.menu.update(dt)

    def render(self, surface):
        """Draw the game over screen."""
        # Draw background
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            # Fill with a dark color
            surface.fill((20, 20, 40))

            # Add some particles or effects based on win/lose state
            self.draw_background_effects(surface)

        # Draw title
        title_x = (self.engine.width - self.title_text.get_width()) // 2
        surface.blit(self.title_text, (title_x, 100))

        # Draw score
        score_x = (self.engine.width - self.score_text.get_width()) // 2
        surface.blit(self.score_text, (score_x, 180))

        # Draw menu
        self.menu.render(surface)

    def draw_background_effects(self, surface):
        """Draw different effects based on win/lose state."""
        if self.win_state:
            # Draw celebratory particles for win
            for _ in range(20):
                x = random.randint(0, self.engine.width)
                y = random.randint(0, self.engine.height)
                size = random.randint(2, 8)
                color = random.choice(
                    [(255, 215, 0), (255, 255, 255), (255, 255, 0)]  # Gold  # White  # Yellow
                )
                pygame.draw.circle(surface, color, (x, y), size)
        else:
            # Draw somber effects for loss
            for y in range(0, self.engine.height, 4):
                alpha = random.randint(10, 30)
                pygame.draw.line(surface, (100, 0, 0, alpha), (0, y), (self.engine.width, y))

    # Button event handlers
    def on_button_hover(self, button):
        """Handle button hover events."""
        if self.sfx_hover and self.engine.settings.sfx_enabled:
            self.sfx_hover.play()

    def on_play_again_clicked(self):
        """Restart the game."""
        if self.sfx_select and self.engine.settings.sfx_enabled:
            self.sfx_select.play()
        self.engine.scene_manager.switch_to("game")

    def on_main_menu_clicked(self):
        """Return to main menu."""
        if self.sfx_select and self.engine.settings.sfx_enabled:
            self.sfx_select.play()
        self.engine.scene_manager.switch_to("main_menu")
