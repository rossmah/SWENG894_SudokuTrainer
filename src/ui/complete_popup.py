# ui/complete_popup.py
import pygame
import ui.style as style

class CompletePopup:
    def __init__(self, time_seconds, difficulty, screen_width, screen_height):
        self.time_seconds = int(time_seconds)
        self.difficulty = difficulty
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = style.get_title_font(48)
        self.text_font = style.get_default_font(24)
        self.button_font = style.get_default_font(20)

        # Button rect (centered, relative to screen)
        self.button_rect = pygame.Rect(
            screen_width // 2 - 150,
            screen_height // 2 + 60,
            300, 48
        )

        # Card geometry
        self.card_w, self.card_h = 560, 260
        self.card_x = self.screen_width//2 - self.card_w//2
        self.card_y = self.screen_height//2 - self.card_h//2
        self.card_rect = pygame.Rect(self.card_x, self.card_y, self.card_w, self.card_h)

        # Active flag
        self.active = True

    def format_time(self):
        mins, secs = divmod(self.time_seconds, 60)
        return f"{mins:02}:{secs:02}"

    def draw(self, screen):
        # If popup is inactive, don't draw
        if not getattr(self, "active", True):
            return

        overlay = pygame.Surface((self.screen_width, self.screen_height), flags=pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))

        card_color = (int(style.BACKGROUND_GRID[0]), int(style.BACKGROUND_GRID[1]), int(style.BACKGROUND_GRID[2]), 240)
        pygame.draw.rect(overlay, card_color, self.card_rect, border_radius=12)

        # card border (opaque)
        pygame.draw.rect(overlay, style.GRID_BLACK_LINE, self.card_rect, 2, border_radius=12)

        # Title
        title_surf = self.title_font.render("Congratulations!", True, style.TEXT_COLOR)
        overlay.blit(title_surf, (self.card_x + self.card_w//2 - title_surf.get_width()//2, self.card_y + 18))

        # Time text
        time_surf = self.text_font.render(f"Time: {self.format_time()}", True, style.TEXT_COLOR)
        overlay.blit(time_surf, (self.card_x + 40, self.card_y + 90))

        # Difficulty text
        diff_surf = self.text_font.render(f"Difficulty: {self.difficulty}", True, style.TEXT_COLOR)
        overlay.blit(diff_surf, (self.card_x + 40, self.card_y + 130))

        # Draw button on overlay
        pygame.draw.rect(overlay, style.BUTTON_BLUE, self.button_rect, border_radius=10)
        btn_text = self.button_font.render("Return to Main Menu", True, style.TEXT_COLOR)
        overlay.blit(btn_text, (self.button_rect.centerx - btn_text.get_width()//2,
                                self.button_rect.centery - btn_text.get_height()//2))

        screen.blit(overlay, (0, 0))

    #
    # Returns:
    #    'menu' if the Return button was clicked,
    #    None otherwise.
    #
    def handle_event(self, event):
        if not getattr(self, "active", True):
            return None

        if event.type == pygame.MOUSEBUTTONUP:
            if self.button_rect.collidepoint(event.pos):
                # mark inactive and return menu action
                self.active = False
                return 'menu'
        return None
