# tests/test_hint_highlighting.py
import pytest
import pygame
from unittest.mock import patch
from ui.hint_section import HintSection

# --- Dummy Board for Testing ---
class DummyBoard:
    def __init__(self):
        self.screen_size = 500
        self.size = 9
        self.user_board = [[0]*9 for _ in range(9)]
        self.notes = [[set() for _ in range(9)] for _ in range(9)]
        self.last_highlight = None
        self.last_eliminations = None

    def highlight_cells(self, highlights):
        self.last_highlight = highlights

    def highlight_eliminations(self, eliminations):
        self.last_eliminations = eliminations

# --- Pygame Initialization ---
@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()

# --- Off-screen Surface Fixture ---
@pytest.fixture
def pygame_screen():
    screen = pygame.Surface((800, 600))  # off-screen surface
    return screen

# --- HintSection Fixture ---
@pytest.fixture
def hint_section():
    board = DummyBoard()
    section = HintSection(board, screen_width=800)
    return section, board

# =====================
# --- TC-12.x: Eliminations ---
# =====================

def test_naked_singles_highlight_elimination(hint_section, pygame_screen):
    section, board = hint_section
    hint = {"cell": (0,0), "value": 5, "eliminations": [{"cell": (0,1), "remove": 3}]}

    with patch("hints.engine.hint_engine.HintEngine.get_all_hints", return_value={"Naked Singles": [hint]}):
        section.open_heuristics["Naked Singles"] = True
        section.draw(pygame_screen)

        rect, h = section.show_button_rects[0]
        board.highlight_cells(h.get("cell"))
        board.highlight_eliminations(h.get("eliminations"))

        assert board.last_eliminations == hint["eliminations"]
        assert board.last_highlight == hint["cell"]

def test_hidden_singles_highlight_elimination(hint_section, pygame_screen):
    section, board = hint_section
    hint = {"cell": (1,2), "value": 4, "eliminations": [{"cell": (1,3), "remove": 7}]}

    with patch("hints.engine.hint_engine.HintEngine.get_all_hints", return_value={"Hidden Singles": [hint]}):
        section.open_heuristics["Hidden Singles"] = True
        section.draw(pygame_screen)

        rect, h = section.show_button_rects[0]
        board.highlight_cells(h.get("cell"))
        board.highlight_eliminations(h.get("eliminations"))

        assert board.last_eliminations == hint["eliminations"]
        assert board.last_highlight == hint["cell"]

def test_naked_pairs_highlight_elimination(hint_section, pygame_screen):
    section, board = hint_section
    hint = {"cell": [(2,0),(2,1)], "value": [3,6], "eliminations": [{"cell": (2,2), "remove": 3}]}

    with patch("hints.engine.hint_engine.HintEngine.get_all_hints", return_value={"Naked Pairs": [hint]}):
        section.open_heuristics["Naked Pairs"] = True
        section.draw(pygame_screen)

        rect, h = section.show_button_rects[0]
        board.highlight_cells(h.get("cell"))
        board.highlight_eliminations(h.get("eliminations"))

        assert board.last_eliminations == hint["eliminations"]
        assert board.last_highlight == hint["cell"]

# =====================
# --- TC-13.x: Candidate Highlights ---
# =====================

def test_naked_singles_show_highlight(hint_section, pygame_screen):
    section, board = hint_section
    hint = {"cell": (0,0), "value": 5, "eliminations": []}

    with patch("hints.engine.hint_engine.HintEngine.get_all_hints", return_value={"Naked Singles": [hint]}):
        section.open_heuristics["Naked Singles"] = True
        section.draw(pygame_screen)

        rect, h = section.show_button_rects[0]
        board.highlight_cells(h.get("cell"))

        assert board.last_highlight == hint["cell"]

def test_hidden_singles_show_highlight(hint_section, pygame_screen):
    section, board = hint_section
    hint = {"cell": (1,1), "value": 7, "eliminations": []}

    with patch("hints.engine.hint_engine.HintEngine.get_all_hints", return_value={"Hidden Singles": [hint]}):
        section.open_heuristics["Hidden Singles"] = True
        section.draw(pygame_screen)

        rect, h = section.show_button_rects[0]
        board.highlight_cells(h.get("cell"))

        assert board.last_highlight == hint["cell"]

def test_naked_pairs_show_highlight(hint_section, pygame_screen):
    section, board = hint_section
    hint = {"cell": [(2,2),(2,3)], "value": [2,9], "eliminations": []}

    with patch("hints.engine.hint_engine.HintEngine.get_all_hints", return_value={"Naked Pairs": [hint]}):
        section.open_heuristics["Naked Pairs"] = True
        section.draw(pygame_screen)

        rect, h = section.show_button_rects[0]
        board.highlight_cells(h.get("cell"))

        assert board.last_highlight == hint["cell"]
