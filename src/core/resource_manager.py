import pygame
from ..utils.logger import GameLogger


class ResourceManager:
    """Manages game assets and resources."""

    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.logger = GameLogger.get_logger("ResourceManager")
        self.logger.info("Resource Manager initialized")

    def load_image(self, name, path, alpha=True):
        """Load an image and store it."""
        try:
            if alpha:
                image = pygame.image.load(path).convert_alpha()
            else:
                image = pygame.image.load(path).convert()
            self.images[name] = image
            self.logger.debug(f"Loaded image: {name} from {path}")
            return image
        except (pygame.error, FileNotFoundError) as e:
            self.logger.error(f"Error loading image {path}: {e}")
            raise FileNotFoundError(f"No such file or directory: '{path}'")

    def get_image(self, name):
        """Retrieve a loaded image."""
        image = self.images.get(name)
        if image is None:
            self.logger.warning(f"Image not found: {name}")
        return image

    def load_sound(self, name, path):
        """Load a sound effect and store it."""
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            self.logger.debug(f"Loaded sound: {name} from {path}")
            return sound
        except (pygame.error, FileNotFoundError) as e:
            self.logger.error(f"Error loading sound {path}: {e}")
            return None

    def get_sound(self, name):
        """Retrieve a loaded sound."""
        sound = self.sounds.get(name)
        if sound is None:
            self.logger.warning(f"Sound not found: {name}")
        return sound

    def load_font(self, name, path, size):
        """Load a font and store it."""
        try:
            font = pygame.font.Font(path, size)
            self.fonts[(name, size)] = font
            self.logger.debug(f"Loaded font: {name} size {size} from {path}")
            return font
        except (pygame.error, FileNotFoundError) as e:
            self.logger.error(f"Error loading font {path}: {e}")
            return None

    def get_font(self, name, size):
        """Retrieve a loaded font."""
        font = self.fonts.get((name, size))
        if font is None:
            self.logger.warning(f"Font '{name}' size {size} not found")
        return font
