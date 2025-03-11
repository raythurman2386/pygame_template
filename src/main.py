import pygame
from src.core.engine import Engine
from src.scenes.credits_scene import CreditsScene
from src.scenes.menu_scene import MainMenuScene
from src.scenes.pong_scene import PongScene
from src.scenes.pause_scene import PauseMenuScene
from src.scenes.options_scene import OptionsMenuScene
from src.scenes.game_over_scene import GameOverScene


def main():
    pygame.font.init()
    engine = Engine(width=800, height=600, title="PyGame Pong Template")

    main_menu = MainMenuScene(engine)
    game_scene = PongScene(engine)
    pause_menu = PauseMenuScene(engine)
    options_menu = OptionsMenuScene(engine, return_scene="main_menu")
    options_from_pause = OptionsMenuScene(engine, return_scene="pause")
    credits_scene = CreditsScene(engine)
    game_over = GameOverScene(engine)

    engine.scene_manager.add_scene("main_menu", main_menu)
    engine.scene_manager.add_scene("credits", credits_scene)
    engine.scene_manager.add_scene("game", game_scene)
    engine.scene_manager.add_scene("pause", pause_menu)
    engine.scene_manager.add_scene("options", options_menu)
    engine.scene_manager.add_scene("options_from_pause", options_from_pause)
    engine.scene_manager.add_scene("game_over", game_over)

    engine.scene_manager.switch_to("main_menu")

    engine.run()


if __name__ == "__main__":
    main()
