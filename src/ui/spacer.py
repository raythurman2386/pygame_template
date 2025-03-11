from .element import UIElement


class Spacer(UIElement):
    """An invisible UI element used for spacing."""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def handle_event(self, event):
        """Spacers don't process events."""
        pass

    def update(self, dt):
        """Spacers don't need updates."""
        pass

    def render(self, surface):
        """Spacers are invisible, so they don't render anything."""
        pass
