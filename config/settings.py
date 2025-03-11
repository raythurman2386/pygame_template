"""Game settings that can be modified during runtime."""

import json

import pygame


class Settings:
    """Stores all modifiable game settings."""

    def __init__(self):
        # Display settings
        self.fullscreen = False
        self.vsync = True
        self.fps_limit = 60

        # Audio settings
        self.master_volume = 1.0
        self.music_volume = 0.8
        self.sfx_volume = 1.0
        self.music_enabled = True
        self.sfx_enabled = True

        # Gameplay settings
        self.difficulty = "normal"

        # Controls
        self.key_bindings = {
            "move_left": pygame.K_LEFT,
            "move_right": pygame.K_RIGHT,
            "jump": pygame.K_SPACE,
            "pause": pygame.K_ESCAPE,
        }

    def save(self, filename="settings.json"):
        """Save settings to a file."""
        data = {
            "display": {
                "fullscreen": self.fullscreen,
                "vsync": self.vsync,
                "fps_limit": self.fps_limit,
            },
            "audio": {
                "master_volume": self.master_volume,
                "music_volume": self.music_volume,
                "sfx_volume": self.sfx_volume,
                "music_enabled": self.music_enabled,
                "sfx_enabled": self.sfx_enabled,
            },
            "gameplay": {"difficulty": self.difficulty},
            "controls": self.key_bindings,
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, filename="settings.json"):
        """Load settings from a file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            # Display settings
            self.fullscreen = data["display"]["fullscreen"]
            self.vsync = data["display"]["vsync"]
            self.fps_limit = data["display"]["fps_limit"]

            # Audio settings
            self.master_volume = data["audio"]["master_volume"]
            self.music_volume = data["audio"]["music_volume"]
            self.sfx_volume = data["audio"]["sfx_volume"]
            self.music_enabled = data["audio"]["music_enabled"]
            self.sfx_enabled = data["audio"]["sfx_enabled"]

            # Gameplay settings
            self.difficulty = data["gameplay"]["difficulty"]

            # Controls
            self.key_bindings = data["controls"]

            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
