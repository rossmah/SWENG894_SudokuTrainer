# tests/test_naked_pairs.py
import pytest
import pygame
from hints.heuristics.naked_pairs import find_naked_pairs
from ui.board import Board

# --- Fixtures ---
@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()  # initializes all pygame modules, including font
    pygame.font.init()
    yield
    pygame.quit()

@pytest.fixture
def empty_board():
    # 9x9 empty board
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    return Board(puzzle=puzzle)

# tests/test_naked_pairs.py
import pytest
from unittest.mock import patch
from hints.heuristics.naked_pairs import find_naked_pairs

# ---------------- Dummy Boards ----------------
class DummyBoard:
    def __init__(self, user_board):
        self.user_board = user_board
        self.size = 9

# ---------------- Test Cases ----------------
def test_detect_naked_pair_in_row():
    # Row 0 has a naked pair (1,2) in columns 0 & 1
    user_board = [[0]*9 for _ in range(9)]
    board = DummyBoard(user_board)

    # Patch get_all_candidates to force the naked pair
    candidates = [[set() for _ in range(9)] for _ in range(9)]
    candidates[0][0] = {1, 2}
    candidates[0][1] = {1, 2}

    with patch("hints.utils.board_utils.get_all_candidates", return_value=candidates):
        findings = find_naked_pairs(board)

    # There should be eliminations in row 0 (columns 2-8) for 1 and 2
    eliminated_cells = [(r-1, c-1) for f in findings for r, c in [f['cell']]]
    expected_cells = [(0, c) for c in range(2, 9)]
    assert all(cell in eliminated_cells for cell in expected_cells), "Naked pair in row not detected"

def test_detect_naked_pair_in_column():
    # Column 0 has a naked pair (3,4) in rows 0 & 1
    user_board = [[0]*9 for _ in range(9)]
    board = DummyBoard(user_board)

    candidates = [[set() for _ in range(9)] for _ in range(9)]
    candidates[0][0] = {3, 4}
    candidates[1][0] = {3, 4}

    with patch("hints.utils.board_utils.get_all_candidates", return_value=candidates):
        findings = find_naked_pairs(board)

    eliminated_cells = [(r-1, c-1) for f in findings for r, c in [f['cell']]]
    expected_cells = [(r, 0) for r in range(2, 9)]
    assert all(cell in eliminated_cells for cell in expected_cells), "Naked pair in column not detected"

def test_detect_naked_pair_in_block():
    # Top-left block has naked pair (5,6) at (0,0) and (1,1)
    user_board = [[0]*9 for _ in range(9)]
    board = DummyBoard(user_board)

    candidates = [[set() for _ in range(9)] for _ in range(9)]
    candidates[0][0] = {5, 6}
    candidates[1][1] = {5, 6}

    with patch("hints.utils.board_utils.get_all_candidates", return_value=candidates):
        findings = find_naked_pairs(board)

    eliminated_cells = [(r-1, c-1) for f in findings for r, c in [f['cell']]]
    # All other cells in block (0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2) should be affected
    expected_cells = [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]
    assert all(cell in eliminated_cells for cell in expected_cells), "Naked pair in block not detected"
