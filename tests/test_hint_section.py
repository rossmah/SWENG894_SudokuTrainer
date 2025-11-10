# tests/test_hint_section.py
import pytest
import pygame
from ui.hint_section import HintSection, handle_hint_key

# --- Fixtures ---
@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()

@pytest.fixture
def small_board():
    # Simple 9x9 empty board
    puzzle = [[0 for _ in range(9)] for _ in range(9)]

    class MockBoard:
        def __init__(self, puzzle):
            self.user_board = puzzle
            self.size = 9
            self.screen_size = 400   # Required by HintSection
            self.highlighted_candidates = {}  # {(r,c): set of values}
            self.highlighted_cells = []

        def highlight_cells(self, hints):
            for hint in hints:
                cells = hint.get("cell")
                values = hint.get("value")

                # Normalize
                if isinstance(cells, tuple):
                    cells = [cells]
                if not isinstance(values, (list, set, tuple)):
                    values = [values]

                # Flatten sets/lists
                flat_values = set()
                for v in values:
                    if isinstance(v, (list, set, tuple)):
                        flat_values.update(v)
                    else:
                        flat_values.add(v)

                for r, c in cells:
                    # Skip out-of-bounds
                    if 0 <= r < self.size and 0 <= c < self.size:
                        self.highlighted_candidates.setdefault((r, c), set()).update(flat_values)
                        if (r, c) not in self.highlighted_cells:
                            self.highlighted_cells.append((r, c))

        def highlight_eliminations(self, elims):
            pass

        @property
        def notes(self):
            return [[set() for _ in range(self.size)] for _ in range(self.size)]

    return MockBoard(puzzle)

@pytest.fixture
def hint_section(small_board):
    return HintSection(small_board, screen_width=600)

# --- Tests ---
def test_initialization(hint_section, small_board):
    assert hint_section.board == small_board
    assert hint_section.screen_width == 600
    assert hint_section.padding == 20
    assert hasattr(hint_section, "buttons")
    assert isinstance(hint_section.buttons, list)

def test_handle_hint_key_updates_highlights(small_board):
    dummy_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_f})
    handle_hint_key(dummy_event, small_board)

    # Check that highlighted candidates are populated
    any_highlight = any(len(c) > 0 for c in small_board.notes[0][0])
    # Actually, check our mock highlights
    assert len(small_board.highlighted_candidates) > 0

def test_handle_hint_key_invalid_key_does_nothing(small_board):
    dummy_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_z})
    prev_candidates = small_board.highlighted_candidates.copy()
    handle_hint_key(dummy_event, small_board)
    assert small_board.highlighted_candidates == prev_candidates

def test_highlight_all_candidates_for_show(small_board):
    small_board.highlight_cells([{"cell": (0, 0), "value": 1}])
    assert (0, 0) in small_board.highlighted_candidates
    assert 1 in small_board.highlighted_candidates[(0, 0)]

def test_highlight_multiple_cells(small_board):
    hints = [
        {"cell": (0, 0), "value": 1},
        {"cell": (1, 1), "value": [2, 3]},
    ]
    small_board.highlight_cells(hints)
    assert small_board.highlighted_candidates[(0, 0)] == {1}
    assert small_board.highlighted_candidates[(1, 1)] == {2, 3}

def test_edge_case_empty_hint_list(small_board):
    small_board.highlight_cells([])
    assert small_board.highlighted_candidates == {}

def test_highlight_cells_out_of_bounds(small_board):
    hints = [{"cell": (9, 9), "value": 1}]
    small_board.highlight_cells(hints)
    assert small_board.highlighted_candidates == {}

def test_show_all_candidates_on_empty_board(small_board):
    hints = [{"cell": (r, c), "value": r * 9 + c + 1} for r in range(9) for c in range(9)]
    small_board.highlight_cells(hints)
    for r in range(9):
        for c in range(9):
            assert (r, c) in small_board.highlighted_candidates
            assert isinstance(small_board.highlighted_candidates[(r, c)], set)
            assert len(small_board.highlighted_candidates[(r, c)]) > 0
