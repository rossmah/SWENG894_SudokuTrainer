# tests/test_hint_section.py
import pytest
import pygame
from unittest.mock import MagicMock
from ui.hint_section import HintSection, handle_hint_key
from ui.board import Board

# --- Fixtures ---
@pytest.fixture
def small_board():
    # Simple 9x9 empty board
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    b = Board(puzzle=puzzle)
    return b

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()  # initializes all pygame modules, including font
    pygame.font.init()
    yield
    pygame.quit()

@pytest.fixture
def hint_section(small_board):
    return HintSection(small_board, screen_width=600)

# --- Tests ---
def test_initialization(hint_section, small_board):
    # Ensure HintSection initializes properly
    assert hint_section.board == small_board
    assert hint_section.screen_width == 600
    assert hint_section.padding == 20

def test_handle_hint_key_updates_highlights(hint_section, small_board):
    # Create a dummy pygame event with a valid key
    dummy_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})

    # Call handle_hint_key
    handle_hint_key(dummy_event, small_board)

    # Check that highlighted cells/candidates are populated
    assert hasattr(small_board, "highlighted_cells")
    assert hasattr(small_board, "highlighted_candidates")
    # Should have at least one candidate highlighted if puzzle is empty
    any_highlight = any(len(c) > 0 for c in small_board.highlighted_candidates.values())
    assert any_highlight

def test_handle_hint_key_invalid_key_does_nothing(hint_section, small_board):
    dummy_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_z})
    prev_cells = small_board.highlighted_cells[:]
    prev_candidates = small_board.highlighted_candidates.copy()

    handle_hint_key(dummy_event, small_board)

    # Invalid key should not change highlights
    assert small_board.highlighted_cells == prev_cells
    assert small_board.highlighted_candidates == prev_candidates

def test_highlight_all_candidates_for_show(hint_section, small_board):
    # Manually call hint_section logic to simulate "Show"
    small_board.highlight_cells([{"cell": (0, 0), "value": 1}])
    
    # Check that all candidates are added to highlighted_candidates
    r, c = 0, 0
    assert (r, c) in small_board.highlighted_candidates
    assert isinstance(small_board.highlighted_candidates[(r, c)], set)
    assert 1 in small_board.highlighted_candidates[(r, c)]

def test_highlight_multiple_cells(hint_section, small_board):
    hints = [
        {"cell": (0, 0), "value": 1},
        {"cell": (1, 1), "value": [2, 3]},
    ]
    small_board.highlight_cells(hints)

    # Check multiple cells are highlighted
    assert (0, 0) in small_board.highlighted_candidates
    assert (1, 1) in small_board.highlighted_candidates
    assert small_board.highlighted_candidates[(0, 0)] == {1}
    assert small_board.highlighted_candidates[(1, 1)] == {2, 3}

def test_edge_case_empty_hint_list(small_board):
    # Should not throw error
    small_board.highlight_cells([])
    assert small_board.highlighted_candidates == {}

def test_highlight_cells_out_of_bounds(small_board):
    # Cell out of bounds should be skipped
    hints = [{"cell": (9, 9), "value": 1}]
    small_board.highlight_cells(hints)
    # No highlights should be added
    assert small_board.highlighted_candidates == {}

def test_show_all_candidates_on_empty_board(small_board):
    # Simulate "Show" all candidates
    hints = [{"cell": (r, c), "value": 1} for r in range(9) for c in range(9)]
    small_board.highlight_cells(hints)
    # Check that every cell has a set of candidates
    for r in range(9):
        for c in range(9):
            assert (r, c) in small_board.highlighted_candidates
            assert isinstance(small_board.highlighted_candidates[(r, c)], set)
            assert len(small_board.highlighted_candidates[(r, c)]) > 0
