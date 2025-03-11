class SceneManager:
    """Manages scene transitions and updates."""

    def __init__(self, engine):
        self.engine = engine
        self.scenes = {}
        self.current_scene = None
        self.current_scene_name = None

    def add_scene(self, name, scene):
        """Register a scene with a name."""
        self.scenes[name] = scene

    def switch_to(self, scene_name):
        """Switch to a different scene."""
        if scene_name not in self.scenes:
            raise ValueError(f"Scene '{scene_name}' not found")

        if self.current_scene:
            self.current_scene.exit()

        self.current_scene_name = scene_name
        self.current_scene = self.scenes[scene_name]
        self.current_scene.enter()

    def handle_event(self, event):
        """Pass events to current scene."""
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self, dt):
        """Update current scene."""
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self, surface):
        """Render current scene."""
        if self.current_scene:
            self.current_scene.render(surface)
