import pygame
import sys
from ui.menu import Menu
from ui.board import Board
from ui.numberpad import NumberPad
from core.generator import generate_sudoku, fill_board
from ui.timer import Timer
import ui.style as style
from ui.sidebar import Sidebar
from ui.hint_section import handle_hint_key

# ------------------- INITIALIZE PYGAME -------------------
# Initialize Pygame
pygame.init()

# ------------------- CONSTANTS -------------------
# Constants
CELL_SIZE = 60
GRID_SIZE = 550
BUTTON_HEIGHT = 60
BUTTON_AREA_HEIGHT = BUTTON_HEIGHT + 20  # padding
SIDEBAR_WIDTH = 300

# Update screen size
SCREEN_WIDTH = GRID_SIZE + SIDEBAR_WIDTH # expand for right menu
SCREEN_HEIGHT = GRID_SIZE + BUTTON_AREA_HEIGHT
GRID_PIXELS = CELL_SIZE * GRID_SIZE  # 600x600 square for grid
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game states
STATE_MENU = "menu"
STATE_DIFFICULTY = "difficulty"
STATE_GAME = "game"

# ------------------- CREATE MENUS -------------------
# Menus
main_menu = Menu(
    [("START NEW GAME", "new_game"),
     ("IMPORT", "import"),
     ("CONTINUE", 'continue'),
     ("QUIT", "quit")], 
     style.FONT_MENU, 
     x=SCREEN_WIDTH // 2, 
     y=SCREEN_HEIGHT // 4,
     menu_type = "MAIN",
     spacing = 60)
difficulty_menu = Menu(
    [("EASY", "easy"),
     ("MEDIUM", "medium"),
     ("HARD", "hard"),
     ("EXPERT", "expert")],
     style.FONT_MENU,
     x=SCREEN_WIDTH // 2, 
     y=SCREEN_HEIGHT // 4,
     menu_type = "DIFFICULTY",
     spacing = 60)

# ------------------- GLOBALS -------------------
clock = pygame.time.Clock()

# State
game_state = STATE_MENU
board = None
selected_difficulty = None
selected_cell = None
timer = None


# Main loop
def main():
    global game_state, board, selected_difficulty, selected_cell, timer

    clock = pygame.time.Clock()
    run = True

    while run:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # --- TIMER HANDLING ---
            if timer:
                timer.handle_event(event)
            
            # If overlay is active, skip other input underneath
            if timer and timer.paused:
                continue

            # --- MAIN MENU ---
            if game_state == STATE_MENU:
                choice = main_menu.handle_event(event)
                if choice == "new_game":
                    game_state = STATE_DIFFICULTY
                elif choice == "quit":
                    run = False

            # --- DIFFICULTY MENU ---
            elif game_state == STATE_DIFFICULTY:
                difficulty_choice = difficulty_menu.handle_event(event)
                if difficulty_choice:
                    # Generate puzzle for selected difficulty
                    puzzle, solution_board = generate_sudoku(difficulty_choice)
                    
                    # Create 9x9 board based on puzzle and solution
                    board = Board(
                        size=9,
                        screen_size=GRID_SIZE,
                        puzzle=puzzle,
                        solution=solution_board,
                    )

                    # Automatically refresh hints whenever board changes
                    board.register_update_listener(lambda: sidebar.hint_section.draw(screen))
                    
                    #DUBUG SECTION - Keeping for easy debug access, for now
                    '''
                    print("Puzzle for difficulty", choice)
                    for row in puzzle:
                        print(row)

                    print("grid type:", type(board.grid), "len:", len(board.grid))
                    print("grid[0] type:", type(board.grid[0]))
                    print("user_board type:", type(board.user_board), "len:", len(board.user_board))
                    print("user_board[0] type:", type(board.user_board[0]))

                    # Debug print
                    print("=== Initial Board State ===")
                    print("grid:")
                    for row in board.grid:
                        print(row)
                    print("user_board:")
                    for row in board.user_board:
                        print(row)
                    print("givens:")
                    for row in board.givens:
                        print(row)
                    print("solutions:")
                    for row in solution_board:
                        print(row)
                    '''

                    game_state = STATE_GAME
                    board.selected_cell = None

                    numberpad = NumberPad(GRID_SIZE, board.screen_size)
                    numberpad.board = board

                    # Kick off game timer
                    timer = Timer(style.FONT_TIMER, 650, 32)
                    timer.start()

                    sidebar = Sidebar(board, numberpad, timer, SCREEN_WIDTH)

            # --- BOARD (GAME LOOP)---
            elif game_state == STATE_GAME:
                if event.type == pygame.MOUSEBUTTONUP:
                    # check if numberpad button was clicked
                    num_clicked = numberpad.handle_event(event)
                    if num_clicked and board and board.selected_cell:
                        board.handle_number_entry(num_clicked)
                    else:
                        # only update selected_cell if the click is on the grid
                        clicked_cell = board.get_cell_from_mouse(event.pos)
                        if clicked_cell is not None:
                            board.selected_cell = clicked_cell
                # let user input numbers
                elif event.type == pygame.KEYDOWN:
                    if board and board.selected_cell:
                        board.handle_key(event.key)
                    # Hint Keys - Used for easy testing/debugging
                    if board:
                        handle_hint_key(event, board)

                # Hint Section - Heuristic Button Click Handling
                if board and sidebar:
                    sidebar.hint_section.handle_event(event, board)
                
        # --- DRAW SECTION ---
        screen.fill(style.BACKGROUND_COLOR)
        if game_state == STATE_MENU:
            main_menu.draw(screen)
        elif game_state == STATE_DIFFICULTY:
            difficulty_menu.draw(screen)
        elif game_state == STATE_GAME and board:
            board.draw(screen)
            sidebar.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
