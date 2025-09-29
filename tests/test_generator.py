# src/tests/test_sudoku.py
import pytest
import pygame
from core import generator
from ui.board import Board
from ui.numberpad import NumberPad

# Initialize pygame once for all tests in this module
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def example_board():
    # small test board with a known solution
    solution = [
        [1,2,3,4,5,6,7,8,9],
        [4,5,6,7,8,9,1,2,3],
        [7,8,9,1,2,3,4,5,6],
        [2,3,4,5,6,7,8,9,1],
        [5,6,7,8,9,1,2,3,4],
        [8,9,1,2,3,4,5,6,7],
        [3,4,5,6,7,8,9,1,2],
        [6,7,8,9,1,2,3,4,5],
        [9,1,2,3,4,5,6,7,8]
    ]
    board = Board(size=9, screen_size=600, solution=solution)
    board.selected_cell = (0, 0)  # select top-left cell

    return board

# -------------------
# Test creating a new Board
# -------------------
def test_create_board():
    board = Board(9, 600)
    assert board.size == 9
    assert board.cell_size == 66  # 600 // 9
    assert len(board.grid) == 9
    assert all(len(row) == 9 for row in board.grid)

def test_board_initially_empty():
    board = Board(9, 600)
    for row in board.grid:
        assert all(cell == 0 for cell in row)

def test_board_has_font():
    board = Board(9, 600)
    assert board.font is not None

# -------------------
# Test generating puzzles by difficulty
# -------------------
@pytest.mark.parametrize("difficulty,expected_min_givens", [
    ("easy", 35),
    ("medium", 28),
    ("hard", 20),
    ("expert", 15)
])
def test_generate_sudoku_difficulty(difficulty, expected_min_givens):
    puzzle, solution = generator.generate_sudoku(difficulty)
    # Count non-zero cells
    givens = sum(cell != 0 for row in puzzle for cell in row)
    # Ensure at least a minimum number of givens
    assert givens >= expected_min_givens
    # Ensure 9x9 size
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)

# -------------------
# CELL ENTRY TESTS
# -------------------

def test_correct_number_locks_cell(example_board):
    # Enter the correct number in a cell
    example_board.handle_key(pygame.K_1)
    assert example_board.user_board[0][0] == 1
    assert example_board.locked[0][0] == 1  # cell should be locked

def test_incorrect_number_allowed(example_board):
    # Enter a wrong number in a different cell
    example_board.selected_cell = (0, 1)
    example_board.handle_key(pygame.K_9)
    assert example_board.user_board[0][1] == 9
    assert example_board.locked[0][1] == 0  # should not lock

def test_replace_entry_allowed(example_board):
    # Enter a wrong number in a cell
    example_board.selected_cell = (0, 2)
    example_board.handle_key(pygame.K_9)
    assert example_board.user_board[0][2] == 9
    # Enter different (wrong) number in cell
    example_board.selected_cell = (0, 2)
    example_board.handle_key(pygame.K_8)
    assert example_board.user_board[0][2] == 8 # Should change value

def test_backspace_clears_entry(example_board):
    # Enter a number and then clear it
    example_board.selected_cell = (0, 1)
    example_board.handle_key(pygame.K_9)
    example_board.handle_key(pygame.K_BACKSPACE)
    assert example_board.user_board[0][1] == 0

# -------------------
# INPUT VALIDATION TESTS
# -------------------

def test_ignore_non_numeric_keys(example_board):
    # Press an invalid key and ensure the cell does not change
    example_board.selected_cell = (0, 2)
    example_board.handle_key(pygame.K_w)  # invalid
    assert example_board.user_board[0][2] == 0

def test_prevent_editing_locked_cells(example_board):
    # Lock a cell manually
    example_board.selected_cell = (1, 0)
    example_board.user_board[1][0] = 4
    example_board.locked[1][0] = True
    example_board.handle_key(pygame.K_5)  # attempt to overwrite
    assert example_board.user_board[1][0] == 4  # value should remain

def test_numberpad_entries_valid_only(example_board):
    # Simulate numberpad entry (1–9)
    example_board.selected_cell = (0, 3)
    example_board.handle_key(pygame.K_5)
    assert example_board.user_board[0][3] == 5
    # Simulate an invalid "numberpad" entry outside 1–9
    # Should ignore (no change)
    example_board.handle_key(pygame.K_0)  # 0 is invalid
    assert example_board.user_board[0][3] == 5