import pytest
import os
import pygame
from ui.numberpad import NumberPad

# Minimal mock Board class
class MockBoard:
    def __init__(self):
        self.notes_mode = False
        self.number_counts = {i: 0 for i in range(1, 10)}
        self.toggle_notes_mode_called = False
    def toggle_notes_mode(self):
        self.toggle_notes_mode_called = True

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def mock_board():
    return MockBoard()

@pytest.fixture
def numberpad(mock_board):
    # Patch SysFont to avoid actual font loading
    class MockFont:
        def render(self, text, antialias, color):
            surface = pygame.Surface((10, 10))
            surface.get_rect()
            return surface
    pygame.font.SysFont = lambda name, size: MockFont()

    np = NumberPad(screen_size=800, board_size=400, board=mock_board)

    # Use real numbers for button positions
    np.buttons = [(i+1, (50*(i+1), 50)) for i in range(9)]
    np.switch_rect = pygame.Rect(10, 10, 50, 30)
    return np

@pytest.fixture
def mock_screen():
    return pygame.Surface((800, 600))

def test_numberpad_initialization(numberpad):
    assert len(numberpad.buttons) == 9
    assert hasattr(numberpad, "switch_rect")
    assert hasattr(numberpad, "mode_label_font")

def test_draw_calls_methods(numberpad, mock_screen):
    numberpad.draw(mock_screen)  # Should run without error

def test_handle_event_number_button(numberpad):
    x, y = numberpad.buttons[0][1]
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(x, y))
    result = numberpad.handle_event(event)
    assert result == 1

def test_handle_event_toggle_switch(numberpad, mock_board):
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=numberpad.switch_rect.center)
    numberpad.handle_event(event)
    assert mock_board.toggle_notes_mode_called

def test_handle_event_no_action(numberpad):
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(0, 0))
    result = numberpad.handle_event(event)
    assert result is None
