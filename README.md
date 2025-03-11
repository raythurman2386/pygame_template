# PyGame Template

A production-ready, object-oriented PyGame template for creating 2D games. This template includes a complete scene management system, UI components, and a simple Pong game implementation to demonstrate the framework's capabilities.

## Features

- **Organized, Modular Architecture** using OOP principles
- **Complete Scene Management System** for smooth game state transitions
  - Main Menu
  - Game Scene (Pong)
  - Pause Menu
  - Options Menu
  - Game Over Screen
  - Credits Screen
- **Resource Management** for loading and caching game assets
- **Customizable UI Component Library**:
  - Buttons
  - Labels
  - Toggle Switches
  - Sliders
  - Dropdowns
  - Menus
- **Game Settings** with save/load functionality
- **Entity Component System** for game objects
- **Screen Resolution and Fullscreen Support**
- **Extensible Design** for creating your own games

## Demo Game: Pong

The template includes a fully functional Pong game to demonstrate the architecture:
- Player vs AI gameplay
- Score tracking
- Collision detection
- Game difficulty settings
- Pause functionality

## Getting Started

### Prerequisites

- Python 3.13
- PyGame 2.6.1

### Installation

```bash
# Clone the repository
git clone https://github.com/raythurman2386/pygame-template.git
cd pygame-template

# Install in development mode
pip install -e .
```

### Running the Game

```bash
# Run from the project root directory
python src/main.py
```

## Project Structure

```
pygame-template/
├── assets/                # Game assets (images, sounds, fonts)
│   ├── audio/
│   ├── fonts/
│   └── images/
├── src/                   # Source code
│   ├── core/              # Core engine components
│   │   ├── engine.py      # Main game engine
│   │   ├── scene_manager.py
│   │   └── resource_manager.py
│   ├── objects/          # Game objects
│   │   ├── entity.py      # Base entity class
│   │   ├── ball.py        # Pong ball entity
│   │   └── paddle.py      # Pong paddle entity
│   ├── scenes/            # Game screens and states
│   │   ├── scene.py       # Base scene class
│   │   ├── main_menu_scene.py
│   │   ├── pong_scene.py
│   │   ├── pause_scene.py
│   │   ├── options_scene.py
│   │   ├── game_over_scene.py
│   │   └── credits_scene.py
│   ├── ui/                # User interface components
│   │   ├── element.py     # Base UI element
│   │   ├── button.py
│   │   ├── label.py
│   │   ├── menu.py
│   │   ├── slider.py
│   │   ├── toggle_button.py
│   │   ├── dropdown.py
│   │   └── spacer.py
│   └── main.py            # Entry point
├── tests/                 # Test suite
├── setup.py               # Package configuration
└── README.md              # This file
```

## Creating Your Own Game

This template provides a foundation for building your own 2D games:

1. **Customize Game Entities**: Create your own game objects by extending the `Entity` class
2. **Design Game Scenes**: Build custom screens by extending the `Scene` class
3. **Add UI Components**: Utilize the existing UI system or extend it for your needs
4. **Configure Settings**: Modify `settings.py` for your game's specific options
5. **Add Assets**: Place your audio, images, and fonts in the `assets/` directory

## Controls for Pong

- **Up Arrow / W**: Move paddle up
- **Down Arrow / S**: Move paddle down
- **Escape**: Pause the game

## Extending the Template

The template was designed to be extended and modified. Here are some ideas:

- Add more game scenes
- Implement additional UI components
- Create custom entity types for your specific game
- Add animation systems
- Implement particle effects
- Add sound effects and music
- Create a level system

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The PyGame community
- Original Pong creators
- Everyone who contributs to this template