# ui/numberpad.py
import pygame

class NumberPad:
    def __init__(self, screen_size):
        self.buttons = []
        self.font = pygame.font.SysFont("arial", 32)
        self.button_size = 48
        self.spacing = 10
        self.y = 590
        self.create_buttons(screen_size)

    def create_buttons(self, SCREEN_WIDTH):
        total_width = 9 * self.button_size + (9 - 1) * self.spacing
        start_x = 35
        
    
        button_size = total_width // 9   # 9 buttons across

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for num, (x, y) in self.buttons:
                dx = event.pos[0] - x
                dy = event.pos[1] - y
                if dx*dx + dy*dy <= (self.button_size // 2) ** 2:  # inside circle
                    return num
        return None
