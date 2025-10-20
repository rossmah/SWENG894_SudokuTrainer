# ui/numberpad.py
import pygame
import ui.style as style

class NumberPad:
    def __init__(self, screen_size, board_size, board=None):
        self.buttons = []
        self.font = pygame.font.SysFont("arial", 32)
        self.button_size = 48
        self.board_size = board_size
        self.spacing = 15
        self.y_offset = 10

        self.board = board
        self.create_buttons()

        # Mode label + toggle button
        self.mode_label_font = pygame.font.SysFont("arial", 22)
        self.mode_label_pos = (screen_size + 30, 60)
        self.switch_rect = pygame.Rect(screen_size + 160, 60, 60, 25)
        
    def create_buttons(self):
        total_width = 9 * self.button_size + 8 * self.spacing # 9 buttons, 8 gaps
        start_x = style.GRID_OFFSET_X + (self.board_size - total_width) // 2 + self.button_size // 2 #35
        y = style.GRID_OFFSET_Y + self.board_size + self.y_offset + self.button_size // 2

        for i in range(1, 10):
            x = start_x + (i - 1) * (self.button_size + self.spacing)
            self.buttons.append((i, (x, y)))  # store center coords

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        for num, (x, y) in self.buttons:
            # Hover effect
            dist = ((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5
            is_hovered = dist <= self.button_size // 2
            color = style.NUMBERPAD_HOVER_COLOR if is_hovered else style.NUMBERPAD_BUTTON_COLOR

            # Draw circle for each button
            pygame.draw.circle(screen, color, (x, y), self.button_size // 2)
            pygame.draw.circle(screen, style.NUMBERPAD_BORDER_COLOR, (x, y), self.button_size // 2, 2)

            # Draw text centered in circle
            text_surface = self.font.render(str(num), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)

            # Draw mode label
            mode_text = f"{'Notes' if self.board and self.board.notes_mode else 'Solve'} Mode"
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
