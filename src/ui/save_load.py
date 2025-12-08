import json
import os
import ui.style as style
from ui.board import Board
from ui.timer import Timer
from ui.numberpad import NumberPad
from ui.sidebar import Sidebar

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAVE_PATH = os.path.join(PROJECT_ROOT, "core", "saves", "saved_game.json")
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

#
#    Saves the current game state to a JSON file.
#    
#    Args:
#        board (Board): The current Board instance.
#        timer (Timer): The Timer instance.
#        difficulty (str): The selected difficulty level.
#
def save_game(board, timer, difficulty):
    if not board or not timer:
        return

    # Prepare board data
    board_data = {
        "user_board": board.user_board,
        "givens": board.givens,
        "locked": board.locked,
        "notes": [[list(n) for n in row] for row in board.notes],
        "solution": board.solution,
    }

    # Prepare timer data
    timer_data = {
        "elapsed_time": timer.get_elapsed(),
    }

    # Combine into one JSON object
    save_data = {
        "board": board_data,
        "timer": timer_data,
        "difficulty": difficulty
    }

    # Write to file
    try:
        with open(SAVE_PATH, "w") as f:
            json.dump(save_data, f, indent=2)
        # Confirm file exists
        if os.path.isfile(SAVE_PATH):
            print(f"Game successfully saved to '{SAVE_PATH}'")
        else:
            print(f"Failed to create file at '{SAVE_PATH}'")
    except Exception as e:
        print(f"Error saving game: {e}")

#
#    Load the saved game from the JSON file.
#    Returns a tuple (board, timer, difficulty) if a saved game exists,
#    or (None, None, None) if no saved game found.
#
def load_game(screen, grid_size, screen_width):
    if not os.path.exists(SAVE_PATH):
        print("No saved game found!")
        return None, None, None

    try:
        with open(SAVE_PATH, "r") as f:
            save_data = json.load(f)

        board_data = save_data["board"]
        timer_data = save_data["timer"]
        difficulty = save_data.get("difficulty", None)

        # Reconstruct the Board
        board = Board(
            size=9,
            screen_size=grid_size,
            puzzle=board_data["user_board"],
            solution=board_data.get("solution")
        )

        # Restore givens, locked cells, and notes
        board.givens = board_data["givens"]
        board.locked = board_data["locked"]
        board.notes = [[set(n) for n in row] for row in board_data["notes"]]

        # Recalculate number_counts
        board.update_number_counts()

        # Reconstruct the Timer
        timer = Timer(style.FONT_TIMER, 650, 32)
        timer.elapsed_time = timer_data.get("elapsed_time", 0)
        timer.start()

        numberpad = NumberPad(grid_size, board.screen_size)
        numberpad.board = board
        sidebar = Sidebar(board, numberpad, timer, screen_width)

        print(f"Game loaded from {SAVE_PATH}")
        return board, timer, numberpad, sidebar, difficulty

    except Exception as e:
        print(f"Error loading saved game: {e}")
        return None, None, None