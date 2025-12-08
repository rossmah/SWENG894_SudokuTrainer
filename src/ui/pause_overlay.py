import pygame
import ui.style as style

class PauseOverlay:
    def __init__(self):
        self.buttons = []   # list of (rect, label)
        self.active = False

    def add_button(self, label, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        self.buttons.append((rect, label))
        return rect

    def draw(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT, timer_text):
        # Background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(style.BACKGROUND_COLOR)
        screen.blit(overlay, (0, 0))

        # Title
        font_big = style.get_title_font(60)
        text = font_big.render("PAUSED", True, style.TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2,
                           SCREEN_HEIGHT//2 - text.get_height()//2 - 50))

        # Timer Snapshot
        font_small = style.get_title_font(30)
        timer_render = font_small.render(timer_text, True, style.TEXT_COLOR)
        screen.blit(timer_render, (SCREEN_WIDTH//2 - timer_render.get_width()//2,
                                   SCREEN_HEIGHT//2 - timer_render.get_height()//2))

        # Buttons
        button_font = style.get_title_font(30)
        for rect, label in self.buttons:
            pygame.draw.rect(screen, style.BUTTON_BLUE, rect, border_radius=50)
            txt = button_font.render(label, True, style.TEXT_COLOR)
            txt_rect = txt.get_rect(center=rect.center)
            screen.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for rect, label in self.buttons:
                if rect.collidepoint(event.pos):
                    return label.lower()
        return None
