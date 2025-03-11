import pygame


class ResourceManager:
    """Manages game assets and resources."""

    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, name, path, alpha=True):
        """Load an image and store it."""
        try:
            if alpha:
                image = pygame.image.load(path).convert_alpha()
            else:
                image = pygame.image.load(path).convert()
            self.images[name] = image
            return image
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            return None

    def get_image(self, name):
        """Retrieve a loaded image."""
        return self.images.get(name)

    def load_sound(self, name, path):
        """Load a sound effect and store it."""
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            return sound
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            return None

    def get_sound(self, name):
        """Retrieve a loaded sound."""
        return self.sounds.get(name)

    def load_font(self, name, path, size):
        """Load a font and store it."""
        try:
            font = pygame.font.Font(path, size)
            self.fonts[(name, size)] = font
            return font
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading font {path}: {e}")
            fallback_font = pygame.font.SysFont(None, size)
            self.fonts[(name, size)] = fallback_font
            return fallback_font

    def get_font(self, name, size):
        """Retrieve a loaded font or create a system font if not found."""
        font = self.fonts.get((name, size))
        if font is None:
            # If font isn't loaded yet, create a system font
            print(f"Font '{name}' size {size} not found, using system font")
            font = pygame.font.SysFont(None, size)
            self.fonts[(name, size)] = font
        return font
