import pygame
import sys
from ui.menu import Menu
from ui.board import Board
from core.generator import generate_sudoku, fill_board

# ------------------- INITIALIZE PYGAME -------------------
# Initialize Pygame
pygame.init()

# ------------------- CONSTANTS -------------------
# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
GRID_PIXELS = CELL_SIZE * GRID_SIZE  # 600x600 square for grid
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# FONTS
TITLE_FONT = pygame.font.SysFont("arial", 48)
MENU_FONT = pygame.font.SysFont("arial", 36)

# Game states
STATE_MENU = "menu"
STATE_DIFFICULTY = "difficulty"
STATE_GAME = "game"

# ------------------- CREATE MENUS -------------------
# Menus
main_menu = Menu([("New Game", "new_game"), ("Import", "import"), ("Continue", 'continue'),("Quit", "quit")], TITLE_FONT, 300, 200)
difficulty_menu = Menu([("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard"), ("Expert", "expert")], MENU_FONT, 300, 200)

# ------------------- GLOBALS -------------------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# State
game_state = STATE_MENU
board = None
selected_difficulty = None
selected_cell = None
difficulty = "Medium"


# Main loop
def main():
    global game_state, board, selected_difficulty

    clock = pygame.time.Clock()
    run = True

    while run:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # --- MAIN MENU ---
            if game_state == STATE_MENU:
                choice = main_menu.handle_event(event)
                if choice == "new_game":
                    game_state = STATE_DIFFICULTY
                elif choice == "quit":
                    run = False

            # --- DIFFICULTY MENU ---
            elif game_state == STATE_DIFFICULTY:
                choice = difficulty_menu.handle_event(event)
                if choice:
                    # Create 9x9 board
                    board = Board(9, SCREEN_WIDTH)

                    #Generate full board first
                    solution_board = [[0]*9 for _ in range(9)]
                    fill_board(solution_board)

                    # Generate puzzle for selected difficulty
                    puzzle = generate_sudoku(choice)
                    board.grid = puzzle

                    #Store solution in board
                    board.solution = solution_board

                    game_state = STATE_GAME
                    selected_cell = None

            # --- BOARD ---
            elif game_state == STATE_GAME:
                if event.type == pygame.MOUSEBUTTONUP:
                    # only highlight when clicked
                    selected_cell = board.get_cell_from_mouse(event.pos)
                    #board.draw(screen, selected_cell)

        # --- DRAW SECTION ---
        screen.fill((255,255,255))
        if game_state == STATE_MENU:
            main_menu.draw(screen)
        elif game_state == STATE_DIFFICULTY:
            difficulty_menu.draw(screen)
        elif game_state == STATE_GAME and board:
            board.draw(screen, selected_cell)


        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
