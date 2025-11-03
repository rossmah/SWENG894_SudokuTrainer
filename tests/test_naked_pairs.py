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

@pytest.fixture
def simple_row_pair_board():
    # Board with a naked pair in row 0 at columns 0 and 1
    puzzle = [
        [0]*9,
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
    # Manually fill notes/candidates for row 0
    board.notes[0][0] = {1, 2}
    board.notes[0][1] = {1, 2}
    board.notes[0][2] = {3}
    return board

@pytest.fixture
def simple_column_pair_board():
    # Naked pair in column 0 at rows 0 and 1
    puzzle = [[0]*9 for _ in range(9)]
    board = Board(puzzle=puzzle)
    board.notes[0][0] = {4, 5}
    board.notes[1][0] = {4, 5}
    return board

@pytest.fixture
def simple_block_pair_board():
    # Naked pair in top-left block
    puzzle = [[0]*9 for _ in range(9)]
    board = Board(puzzle=puzzle)
    board.notes[0][0] = {6, 7}
    board.notes[1][1] = {6, 7}
    return board

# --- Tests ---
def test_no_pairs_on_empty_board(empty_board):
    findings = find_naked_pairs(empty_board)
    assert findings == []

def test_detect_naked_pair_in_row(simple_row_pair_board):
    findings = find_naked_pairs(simple_row_pair_board)
    assert len(findings) > 0
    pair_found = False
    for f in findings:
        # Check that technique is Naked Pair
        assert f["technique"] == "Naked Pair"
        # Check cells match the expected row positions
        if f["cell"] == [(0, 0), (0, 1)] or f["cell"] == [(0, 1), (0, 0)]:
            pair_found = True
            # Check value set
            assert f["value"] == {1, 2}
            # Check scope
            assert "row" in f["where"]
    assert pair_found

def test_detect_naked_pair_in_column(simple_column_pair_board):
    findings = find_naked_pairs(simple_column_pair_board)
    pair_found = False
    for f in findings:
        if f["cell"] == [(0, 0), (1, 0)] or f["cell"] == [(1, 0), (0, 0)]:
            pair_found = True
            assert f["value"] == {4, 5}
            assert "column" in f["where"]
    assert pair_found

def test_detect_naked_pair_in_block(simple_block_pair_board):
    findings = find_naked_pairs(simple_block_pair_board)
    pair_found = False
    for f in findings:
        if f["cell"] == [(0, 0), (1, 1)] or f["cell"] == [(1, 1), (0, 0)]:
            pair_found = True
            assert f["value"] == {6, 7}
            assert "block" in f["where"]
    assert pair_found

def test_multiple_pairs():
    # Board with multiple pairs in different units
    puzzle = [[0]*9 for _ in range(9)]
    board = Board(puzzle=puzzle)
    # Row pair
    board.notes[0][0] = {1, 2}
    board.notes
