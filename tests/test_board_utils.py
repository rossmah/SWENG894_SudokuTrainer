# tests/test_board_utils.py
import pytest
import pygame
from io import StringIO
import sys
from hints.utils import board_utils as bu

# --- Mock Board ---
class MockBoard:
    def __init__(self, user_board):
        self.user_board = user_board
        self.size = len(user_board)

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()  # initializes all pygame modules, including font
    pygame.font.init()
    yield
    pygame.quit()
    
@pytest.fixture
def sample_board():
    # 3x3 block board for simplicity
    board = [
        [1, 0, 3, 0, 0, 6, 0, 8, 9],
        [0, 0, 0, 4, 0, 0, 7, 0, 0],
        [0, 2, 0, 0, 5, 0, 0, 0, 0],
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9,
        [0]*9
    ]
    return MockBoard(board)

# --- Tests ---
def test_cell_to_ui_cell():
    cells = [(0,0),(1,2)]
    result = bu.cell_to_ui_cell(cells)
    assert result == [(1,1),(2,3)]

def test_get_block_bounds():
    assert bu.get_block_bounds(0,0) == (0,3,0,3)
    assert bu.get_block_bounds(4,7) == (3,6,6,9)
    assert bu.get_block_bounds(8,8) == (6,9,6,9)

def test_get_block_values(sample_board):
    values = bu.get_block_values(sample_board, 0, 0)
    assert values == {1,2,3}

    values = bu.get_block_values(sample_board, 1, 4)
    # Top-middle block: 0,3-5 and 0-2
    assert values == {4,5,6}

def test_get_row_values(sample_board):
    row_vals = bu.get_row_values(sample_board, 0)
    assert row_vals == {1,3,6,8,9}
    row_vals = bu.get_row_values(sample_board, 1)
    assert row_vals == {4,7}

def test_get_col_values(sample_board):
    col_vals = bu.get_col_values(sample_board, 0)
    assert col_vals == {1}
    col_vals = bu.get_col_values(sample_board, 1)
    assert col_vals == {2}

def test_get_candidates_for_cell(sample_board):
    # Cell (0,1) has candidates 2,4,5,7
    candidates = bu.get_candidates_for_cell(sample_board, 0,1)
    # All numbers 1-9 minus row, col, block values
    expected = set(range(1,10)) - {1,3,6,8,9,2}
    assert candidates == expected

    # Filled cell should return empty set
    assert bu.get_candidates_for_cell(sample_board,0,0) == set()

def test_get_all_candidates(sample_board):
    candidates = bu.get_all_candidates(sample_board)
    assert len(candidates) == 9
    assert len(candidates[0]) == 9
    # Filled cell should have empty set
    assert candidates[0][0] == set()
    # Empty cell should have set
    assert len(candidates[0][1]) > 0

def test_pretty_print_findings(capsys):
    findings = [
        {"technique":"Hidden Single", "cell":(1,1), "value":5, "reason":"test reason"}
    ]
    bu.pretty_print_findings(findings)
    captured = capsys.readouterr()
    assert "Hidden Single: Cell (1, 1) -> 5 | test reason" in captured.out

def test_pretty_print_findings_empty(capsys):
    bu.pretty_print_findings([])
    captured = capsys.readouterr()
    assert "No hints found." in captured.out
