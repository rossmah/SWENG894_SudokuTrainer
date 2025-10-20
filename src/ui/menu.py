# ui/menu.py
import pygame
import ui.style as style

class Menu:
    def __init__(self, items, font, x, y, menu_type, spacing=50):
        self.items = items          # list of (label, action)
        self.font = font
        self.x = x
        self.y = y
        self.menu_type = menu_type

        # Title Text
        self.title_font = style.get_title_font(80)
        self.title_text = self.title_font.render("SUDOKU TRAINER", True, style.TEXT_COLOR)
        self.title_rect = self.title_text.get_rect(center=(x, 80))
        
        # Select Text
        self.select_font = style.get_default_font(36)
        self.select_text = self.select_font.render("Select Puzzle Difficulty:", True, style.TEXT_COLOR)
        self.select_rect = self.select_text.get_rect(center=(x, 240))
        
        self.spacing = spacing
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        #Turn items into rendered buttons
        for i, (label, action) in enumerate(self.items):
            text_surface = self.font.render(label, True, (0, 0, 0))
            rect = text_surface.get_rect(center=(self.x, self.y + i * self.spacing + 150))
            self.buttons.append((text_surface, rect, action))

    def draw(self, screen):
        screen.blit(self.title_text, self.title_rect)

        if self.menu_type == 'DIFFICULTY':
            screen.blit(self.select_text, self.select_rect)
        for text, rect, _ in self.buttons:
            screen.blit(text, rect)

    def handle_event(self, event):
        #Return the action if a button is clicked, else None
        if event.type == pygame.MOUSEBUTTONUP:
            for _, rect, action in self.buttons:
                if rect.collidepoint(event.pos):
                    return action
        return None