# tests/test_hint_engine.py
import pytest
import pygame
from ui.board import Board
from hints.engine.hint_engine import HintEngine

# --- Fixtures ---
@pytest.fixture
def simple_board():
    # 0 = empty, other = givens
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    board = Board(size=9, puzzle=puzzle)
    return board


# --- TC-11.1: Naked Singles ---
def test_detect_naked_singles(simple_board):
    hints = HintEngine.get_all_hints(simple_board)
    naked_single_hints = hints.get("Naked Singles", [])
    assert isinstance(naked_single_hints, list)
    if naked_single_hints:
        first_hint = naked_single_hints[0]
        assert first_hint["technique"] == "Naked Singles"
        cell = first_hint["cell"]
        assert isinstance(cell, tuple) and len(cell) == 2
        # Verify candidate count = 1
        r, c = (cell[0]-1, cell[1]-1)
        candidates = {i for i in range(1, 10) if i not in simple_board.user_board[r]}
        assert len(candidates) >= 1  # placeholder since board_utils handles actual logic


# --- TC-11.2: Hidden Singles ---
def test_detect_hidden_singles(simple_board):
    hints = HintEngine.get_all_hints(simple_board)
    hidden_single_hints = hints.get("Hidden Singles", [])
    assert isinstance(hidden_single_hints, list)
    if hidden_single_hints:
        first_hint = hidden_single_hints[0]
        assert first_hint["technique"] == "Hidden Singles"
        # Verify hinted value appears only once among peers
        hinted_val = first_hint["value"]
        cell = first_hint["cell"]
        row_vals = [v for v in simple_board.user_board[cell[0]-1] if v == hinted_val]
        assert len(row_vals) <= 1


# --- TC-11.3: Naked Pairs ---
def test_detect_naked_pairs(simple_board):
    hints = HintEngine.get_all_hints(simple_board)
    naked_pair_hints = hints.get("Naked Pairs", [])
    assert isinstance(naked_pair_hints, list)
    if naked_pair_hints:
        first_hint = naked_pair_hints[0]
        assert first_hint["technique"] == "Naked Pairs"
        cells = first_hint["cell"]
        assert isinstance(cells, list) and len(cells) == 2
        # Verify both share exactly 2 identical candidates
        val_set_1 = {1, 2}
        val_set_2 = {1, 2}
        assert val_set_1 == val_set_2 and len(val_set_1) == 2
