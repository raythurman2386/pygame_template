import pygame
from .element import UIElement
from .button import Button
from .label import Label
from .spacer import Spacer


class Menu(UIElement):
    """Container for UI elements arranged vertically."""

    def __init__(self, x, y, width, height, centered=False):
        super().__init__(x, y, width, height)
        self.centered = centered
        self.elements = []
        self.font = None
        self.spacing = 10  # Space between elements

        # Event handlers
        self.on_hover = None  # Called when a button is hovered

    def set_font(self, font):
        """Set font for all menu elements."""
        self.font = font
        for element in self.elements:
            if hasattr(element, "set_font"):
                element.set_font(font)

    def add_element(self, element):
        """Add a UI element to the menu."""
        if self.font and hasattr(element, "set_font"):
            element.set_font(self.font)

        # Position the element
        if len(self.elements) == 0:
            next_y = self.rect.y
        else:
            last_element = self.elements[-1]
            next_y = last_element.rect.y + last_element.rect.height + self.spacing

        element.rect.x = self.rect.x - (element.rect.width // 2 if self.centered else 0)
        element.rect.y = next_y

        self.elements.append(element)
        return element

    def add_button(self, text, callback=None):
        """Add a button with the given text and callback."""
        button = Button(
            x=0,
            y=0,  # Will be positioned by add_element
            width=self.rect.width - 20,
            height=40,
            text=text,
            callback=callback,
        )
        return self.add_element(button)

    def add_label(self, text):
        """Add a text label."""
        label = Label(
            x=0,
            y=0,  # Will be positioned by add_element
            width=self.rect.width - 20,
            height=30,
            text=text,
        )
        return self.add_element(label)

    def add_spacer(self, height):
        """Add empty space of given height."""
        spacer = Spacer(
            x=0, y=0, width=self.rect.width, height=height  # Will be positioned by add_element
        )
        return self.add_element(spacer)

    def handle_event(self, event):
        """Pass events to all elements."""
        for element in self.elements:
            if hasattr(element, "handle_event"):
                element.handle_event(event)

                # Check for hover state change on buttons
                if isinstance(element, Button) and element.hover and self.on_hover:
                    self.on_hover(element)

    def update(self, dt):
        """Update all elements."""
        for element in self.elements:
            if hasattr(element, "update"):
                element.update(dt)

    def render(self, surface):
        """Draw all elements."""
        for element in self.elements:
            if hasattr(element, "render"):
                element.render(surface)
