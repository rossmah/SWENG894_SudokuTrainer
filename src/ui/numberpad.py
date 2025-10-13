# ui/numberpad.py
import pygame

class NumberPad:
    def __init__(self, screen_size, board=None):
        self.buttons = []
        self.font = pygame.font.SysFont("arial", 32)
        self.button_size = 48
        self.spacing = 10
        self.y = 590

        self.board = board
        self.toggle_rect = pygame.Rect(screen_size + 35, 50, 120, 30)
        self.create_buttons(screen_size)

        # Mode label + toggle button
        self.mode_label_font = pygame.font.SysFont("arial", 22)
        self.mode_label_pos = (screen_size + 30, 45)
        self.switch_rect = pygame.Rect(screen_size + 160, 45, 60, 25)
        
    def create_buttons(self, SCREEN_WIDTH):
        total_width = 9 * self.button_size + (9 - 1) * self.spacing
        start_x = 35

        for i in range(1, 10):
            x = start_x + (i - 1) * (self.button_size + self.spacing)
            self.buttons.append((i, (x, self.y)))  # store center coords

    def draw(self, screen):
        for num, (x, y) in self.buttons:
            # Draw circle for each button
            pygame.draw.circle(screen, (200, 200, 200), (x, y), self.button_size // 2)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), self.button_size // 2, 2)

            # Draw text centered in circle
            text_surface = self.font.render(str(num), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)

            # Draw mode label
            mode_text = f"Mode: {'Notes' if self.board and self.board.notes_mode else 'Solve'}"
            mode_label = self.mode_label_font.render(mode_text, True, (0, 0, 0))
            screen.blit(mode_label, self.mode_label_pos)

            # Draw switch button
            pygame.draw.rect(screen, (220, 220, 220), self.switch_rect, border_radius=6)
            pygame.draw.rect(screen, (0, 0, 0), self.switch_rect, 2, border_radius=6)

            # Draw arrows inside switch
            cx, cy = self.switch_rect.center
            arrow_size = 7
            left_arrow = [(cx - 14, cy), (cx - 6, cy - arrow_size), (cx - 6, cy + arrow_size)]
            right_arrow = [(cx + 14, cy), (cx + 6, cy - arrow_size), (cx + 6, cy + arrow_size)]
            pygame.draw.polygon(screen, (0, 0, 0), left_arrow)
            pygame.draw.polygon(screen, (0, 0, 0), right_arrow)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            # Check number buttons
            for num, (x, y) in self.buttons:
                dx = event.pos[0] - x
                dy = event.pos[1] - y
                if dx*dx + dy*dy <= (self.button_size // 2) ** 2:  # inside circle
                    return num
                
            # Check toggle button
            if self.board and self.switch_rect.collidepoint(event.pos):
                self.board.toggle_notes_mode()
        return None
