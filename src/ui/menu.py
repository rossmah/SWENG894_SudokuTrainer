# ui/menu.py
import pygame

class Menu:
    def __init__(self, items, font, x, y, spacing=50):
        self.items = items          # list of (label, action)
        self.font = font
        self.x = x
        self.y = y
        self.spacing = spacing
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        #Turn items into rendered buttons
        for i, (label, action) in enumerate(self.items):
            text_surface = self.font.render(label, True, (0, 0, 0))
            rect = text_surface.get_rect(center=(self.x, self.y + i * self.spacing))
            self.buttons.append((text_surface, rect, action))

    def draw(self, screen):
        for text, rect, _ in self.buttons:
            screen.blit(text, rect)

    def handle_event(self, event):
        #Return the action if a button is clicked, else None
        if event.type == pygame.MOUSEBUTTONUP:
            for _, rect, action in self.buttons:
                if rect.collidepoint(event.pos):
                    return action
        return None