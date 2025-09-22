# src/tests/test_sudoku.py
import pytest
import pygame
from core import generator
from ui.board import Board

# Initialize pygame once for all tests in this module
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

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
    puzzle = generator.generate_sudoku(difficulty)
    # Count non-zero cells
    givens = sum(cell != 0 for row in puzzle for cell in row)
    # Ensure at least a minimum number of givens
    assert givens >= expected_min_givens
    # Ensure 9x9 size
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
