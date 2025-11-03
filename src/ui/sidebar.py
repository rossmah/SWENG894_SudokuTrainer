# ui/sidebar.py
import pygame
import ui.style as style
from ui.hint_section import HintSection

class Sidebar:
    def __init__(self, board, numberpad, timer, screen_width, x_offset=20, y_offset=20):
        self.board = board
        self.numberpad = numberpad
        self.timer = timer
        self.screen_width = screen_width

        # Offsets for sidebar elements
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.spacing = 20  # vertical spacing between elements
        self.padding = 10  # padding between grid and hint panel / screen edge

        # Pre-render title
        self.title_font = style.get_title_font(28)
        self.title_surface = self.title_font.render("SUDOKU TRAINER", True, style.TEXT_COLOR)

        # Position title centered between board and screen edge
        sidebar_width = screen_width - board.screen_size
        self.title_rect = self.title_surface.get_rect(
            center=(board.screen_size + sidebar_width // 2, y_offset + self.title_surface.get_height() // 2)
        )

        self.hint_section = HintSection(board, screen_width)

    def draw(self, screen):
        # Draw title
        title_surface = style.get_title_font(28).render("SUDOKU TRAINER", True, style.TEXT_COLOR)
        screen.blit(title_surface, (self.board.screen_size + 20, 1))

        # Draw timer below title
        if self.timer:
            timer_y = self.title_rect.bottom + self.spacing
            self.timer.draw(screen, self.screen_width, screen.get_height(), style.FONT_TIMER)
        
        # Draw Hint Section
        if self.hint_section and not self.timer.paused:
            self.hint_section.draw(screen)

        # Draw numberpad / toggle button if applicable
        if self.numberpad and not self.timer.paused:
            self.numberpad.draw(screen)