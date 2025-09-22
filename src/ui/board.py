# ui/board.py
import pygame


GRID_LINE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 255)  # for selected cell
GIVEN_COLOR = (0, 0, 0)      # black for givens
USER_COLOR = (50, 50, 200)   # optional color if later we let user enter numbers


class Board:
    def __init__(self, size=9, screen_size=600):
        self.size = size
        self.screen_size = screen_size
        self.cell_size = screen_size // size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.solution = None # stored the solved board for verification
        self.font = pygame.font.SysFont("arial", self.cell_size // 2)

    def draw(self, screen, selected_cell=None):
        # Fill background
        screen.fill((255, 255, 255))

        # Draw grid cells
        for row in range(self.size):
            for col in range(self.size):
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                # Highlight selected cell
                if selected_cell == (row, col):
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect)

                # draw border
                pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)

                # Draw number if present
                num = self.grid[row][col]
                if num != 0:
                    label = self.font.render(str(num), True, GIVEN_COLOR)
                    label_rect = label.get_rect(center=rect.center)
                    screen.blit(label, label_rect)

        # Draw thicker lines every 3 cells (classic Sudoku style)
        for i in range(self.size + 1):
            line_width = 3 if i % 3 == 0 else 1
            # Vertical lines
            pygame.draw.line(
                screen, GRID_LINE_COLOR,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.screen_size),
                line_width
            )
            # Horizontal lines
            pygame.draw.line(
                screen, GRID_LINE_COLOR,
                (0, i * self.cell_size),
                (self.screen_size, i * self.cell_size),
                line_width
            )

    def get_cell_from_mouse(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.size and 0 <= col < self.size:
            return (row, col)
        return None
