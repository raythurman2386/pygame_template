class Scene:
    """Base class for all game scenes."""

    def __init__(self, engine):
        self.engine = engine

    def enter(self):
        """Called when this scene becomes active."""
        pass

    def exit(self):
        """Called when this scene is no longer active."""
        pass

    def handle_event(self, event):
        """Process a pygame event."""
        pass

    def update(self, dt):
        """Update scene state."""
        pass

    def render(self, surface):
        """Render scene to the given surface."""
        pass
