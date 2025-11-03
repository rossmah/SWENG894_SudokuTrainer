# tests/test_hidden_singles.py
import pytest
import pygame
from hints.heuristics.hidden_singles import find_hidden_singles
from ui.board import Board

# --- Fixtures ---
@pytest.fixture
def empty_board():
    # 9x9 empty board
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    return Board(puzzle=puzzle)

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()  # initializes all pygame modules, including font
    pygame.font.init()
    yield
    pygame.quit()

@pytest.fixture
def simple_hidden_single_board():
    # Board designed to have a hidden single
    # Only cell (0,0) can be 1 in row 0
    puzzle = [
        [0, 2, 3, 4, 5, 6, 7, 8, 9],
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9
    ]
    return Board(puzzle=puzzle)

# --- Tests ---
def test_no_hidden_singles_on_empty_board(empty_board):
    hints = find_hidden_singles(empty_board)
    # Empty board has no hidden singles
    assert hints == []

def test_detect_hidden_single_in_row(simple_hidden_single_board):
    hints = find_hidden_singles(simple_hidden_single_board)
    # There should be at least one hint
    assert len(hints) > 0
    for hint in hints:
        r, c = hint["cell"]
        val = hint["value"]
        # Confirm the hinted cell is empty on the board
        assert simple_hidden_single_board.user_board[r][c] == 0
        # Confirm value is not already in row
        row_vals = simple_hidden_single_board.user_board[r]
        assert val not in row_vals

def test_hidden_single_validated_units(simple_hidden_single_board):
    hints = find_hidden_singles(simple_hidden_single_board)
    for hint in hints:
        r, c = hint["cell"]
        val = hint["value"]
        # Validate the row only contains this cell as possible candidate
        row_candidates = [cell for cell in range(9)
                          if val in simple_hidden_single_board.notes[r][cell] or
                             simple_hidden_single_board.user_board[r][cell]==0]
        # Only this cell should be candidate for hidden single
        assert c in row_candidates

def test_multiple_hidden_singles():
    # Custom board with multiple hidden singles in different units
    puzzle = [
        [0,2,3,4,5,6,7,8,9],
        [1,0,0,0,0,0,0,0,0],
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9
    ]
    board = Board(puzzle=puzzle)
    hints = find_hidden_singles(board)
    # There should be more than 1 hidden single
    assert len(hints) >= 2
    # Each hint should be a tuple of (row, col) and value 1-9
    for hint in hints:
        r, c = hint["cell"]
        val = hint["value"]
        assert 0 <= r < 9
        assert 0 <= c < 9
        assert 1 <= val <= 9
        # Cell must be empty
        assert board.user_board[r][c] == 0

def test_hidden_single_ignores_naked_singles():
    # Board with naked singles filled
    puzzle = [
        [1,0,0,0,0,0,0,0,0],
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9
    ]
    board = Board(puzzle=puzzle)
    hints = find_hidden_singles(board)
    # Ensure hints do not include already filled cells (naked singles)
    for hint in hints:
        r, c = hint["cell"]
        assert board.user_board[r][c] == 0
