# tests/test_naked_pairs.py
import pytest
import pygame
from hints.heuristics.naked_pairs import find_naked_pairs
from ui.board import Board
from hints.utils.elimination_utils import find_eliminations

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
    # --- Arrange ---
    user_board = [[0 for _ in range(9)] for _ in range(9)]
    board = DummyBoard(user_board)

    # Only the naked pair cells have the pair {1,2}
    candidates = [[set() for _ in range(9)] for _ in range(9)]
    candidates[0][0] = {1, 2}  # Naked pair cell 1
    candidates[0][1] = {1, 2}  # Naked pair cell 2

    # All other cells in row 0 do not contain 1 or 2
    for c in range(2, 9):
        candidates[0][c] = {3, 4, 5}  # arbitrary other candidates

    # --- Act ---
    with patch("hints.heuristics.naked_pairs.get_all_candidates", return_value=candidates), \
         patch("hints.utils.elimination_utils.find_eliminations", wraps=find_eliminations):
        findings = find_naked_pairs(board)

    # --- Assert ---
    # Collect all eliminated cells from the findings
    eliminated_cells = [(e["cell"][0]-1, e["cell"][1]-1) for f in findings for e in f["eliminations"]]

    # Expect eliminations in row 0 for all cells except the naked pair
    expected_cells = [(0, c) for c in range(2, 9)]
    assert all(cell in eliminated_cells for cell in expected_cells), "Naked pair in row not detected"




def test_detect_naked_pair_in_column():
    # --- Arrange ---
    user_board = [[0 for _ in range(9)] for _ in range(9)]
    board = DummyBoard(user_board)

    # Naked pair in column 0 (rows 0 & 1)
    candidates = [[set() for _ in range(9)] for _ in range(9)]
    candidates[0][0] = {3, 4}
    candidates[1][0] = {3, 4}
    # Other cells in column 0 do not contain 3 or 4
    for r in range(2, 9):
        candidates[r][0] = {1, 2, 5}  # arbitrary other candidates

    # --- Act ---
    with patch("hints.heuristics.naked_pairs.get_all_candidates", return_value=candidates), \
         patch("hints.utils.elimination_utils.find_eliminations", wraps=find_eliminations):
        findings = find_naked_pairs(board)

    # --- Assert ---
    eliminated_cells = [(e["cell"][0]-1, e["cell"][1]-1) for f in findings for e in f["eliminations"]]
    expected_cells = [(r, 0) for r in range(2, 9)]
    assert all(cell in eliminated_cells for cell in expected_cells), "Naked pair in column not detected"

def test_detect_naked_pair_in_block():
    # --- Arrange ---
    user_board = [[0 for _ in range(9)] for _ in range(9)]
    board = DummyBoard(user_board)

    # Naked pair in top-left block (0,0) & (1,1)
    candidates = [[set() for _ in range(9)] for _ in range(9)]
    candidates[0][0] = {5, 6}
    candidates[1][1] = {5, 6}
    # Other cells in the block do not contain 5 or 6
    for r in range(3):
        for c in range(3):
            if (r, c) not in [(0, 0), (1, 1)]:
                candidates[r][c] = {1, 2, 3}  # arbitrary other candidates

    # --- Act ---
    with patch("hints.heuristics.naked_pairs.get_all_candidates", return_value=candidates), \
         patch("hints.utils.elimination_utils.find_eliminations", wraps=find_eliminations):
        findings = find_naked_pairs(board)

    # --- Assert ---
    eliminated_cells = [(e["cell"][0]-1, e["cell"][1]-1) for f in findings for e in f["eliminations"]]
    expected_cells = [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]
    assert all(cell in eliminated_cells for cell in expected_cells), "Naked pair in block not detected"
