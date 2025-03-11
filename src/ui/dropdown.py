import pygame
from .element import UIElement
from .label import Label


class Dropdown(UIElement):
    """A dropdown selection menu."""

    def __init__(self, x, y, width, height, options=None, initial_selection=None, label=None):
        super().__init__(x, y, width, height)
        self.options = options or []
        if initial_selection and initial_selection in self.options:
            self.selected_option = initial_selection
        else:
            self.selected_option = self.options[0] if self.options else ""

        self.is_open = False
        self.hover = False
        self.label_text = label
        self.label = None
        self.font = None
        self.option_height = height

        # Colors
        self.background_color = (80, 80, 80)
        self.hover_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.border_color = (120, 120, 120)

        # Option rects (used when dropdown is open)
        self.option_rects = []

        # Create label if specified
        if label:
            self.label = Label(
                x=x, y=y - 25, width=width, height=20, text=label  # Position above dropdown
            )

    def set_font(self, font):
        """Set font for the dropdown and its label."""
        self.font = font
        if self.label:
            self.label.set_font(font)

    def update_option_rects(self):
        """Update the rectangles for each option."""
        self.option_rects = []
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + self.rect.height + (i * self.option_height),
                self.rect.width,
                self.option_height,
            )
            self.option_rects.append(option_rect)

    def select_option(self, option):
        """Select a specific option."""
        if option in self.options:
            self.selected_option = option
            self.is_open = False

    def handle_event(self, event):
        """Process mouse events."""
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    # Toggle dropdown
                    self.is_open = not self.is_open
                    if self.is_open:
                        self.update_option_rects()
                elif self.is_open:
                    # Check if an option was clicked
                    for i, option_rect in enumerate(self.option_rects):
                        if option_rect.collidepoint(event.pos):
                            self.select_option(self.options[i])
                            break
                    else:
                        # Click outside closes the dropdown
                        self.is_open = False

    def update(self, dt):
        """Update dropdown state."""
        pass

    def render(self, surface):
        """Draw the dropdown control."""
        if not self.visible:
            return

        # Draw label if available
        if self.label:
            self.label.render(surface)

        # Draw the dropdown box
        pygame.draw.rect(
            surface, self.hover_color if self.hover else self.background_color, self.rect
        )
        pygame.draw.rect(surface, self.border_color, self.rect, 2)

        # Draw the selected option
        if self.font:
            text_surface = self.font.render(self.selected_option, True, self.text_color)
            text_x = self.rect.x + 10  # 10px left margin
            text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
            surface.blit(text_surface, (text_x, text_y))

        # Draw dropdown arrow
        arrow_size = 8
        arrow_x = self.rect.x + self.rect.width - arrow_size - 10  # 10px right margin
        arrow_y = self.rect.y + (self.rect.height - arrow_size) // 2

        # Draw triangle pointing down or up based on dropdown state
        points = []
        if self.is_open:
            # Up arrow
            points = [
                (arrow_x, arrow_y + arrow_size),
                (arrow_x + arrow_size, arrow_y + arrow_size),
                (arrow_x + arrow_size // 2, arrow_y),
            ]
        else:
            # Down arrow
            points = [
                (arrow_x, arrow_y),
                (arrow_x + arrow_size, arrow_y),
                (arrow_x + arrow_size // 2, arrow_y + arrow_size),
            ]

        pygame.draw.polygon(surface, self.text_color, points)

        # Draw dropdown options if open
        if self.is_open:
            for i, (option, option_rect) in enumerate(zip(self.options, self.option_rects)):
                # Determine if mouse is hovering over this option
                mouse_pos = pygame.mouse.get_pos()
                is_option_hover = option_rect.collidepoint(mouse_pos)

                # Draw option background
                pygame.draw.rect(
                    surface,
                    self.hover_color if is_option_hover else self.background_color,
                    option_rect,
                )
                pygame.draw.rect(surface, self.border_color, option_rect, 1)

                # Draw option text
                if self.font:
                    text_surface = self.font.render(option, True, self.text_color)
                    text_x = option_rect.x + 10  # 10px left margin
                    text_y = option_rect.y + (option_rect.height - text_surface.get_height()) // 2
                    surface.blit(text_surface, (text_x, text_y))
