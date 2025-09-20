import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 255)
FPS = 60

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Trainer")

# Track selected cell
selected_cell = None  

def draw_grid():
    """Draw a 9x9 Sudoku grid with bold lines every 3 cells."""
    for i in range(GRID_SIZE + 1):
        line_width = 3 if i % 3 == 0 else 1
        # Vertical line
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), line_width)
        # Horizontal line
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), line_width)

def highlight_cell(row, col):
    """Highlight the clicked cell."""
    rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect)

def get_cell_from_mouse(pos):
    """Convert mouse click position to grid row/col."""
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

# Main loop
def main():
    global selected_cell
    clock = pygame.time.Clock()
    run = True

    while run:
        screen.fill(BACKGROUND_COLOR)

        # Highlight selected cell
        if selected_cell is not None:
            highlight_cell(*selected_cell)

        # Draw grid
        draw_grid()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    selected_cell = get_cell_from_mouse(event.pos)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
