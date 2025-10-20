# tests/test_numberpad.py
import pytest
import os
from unittest.mock import MagicMock, patch
import pygame
from ui.numberpad import NumberPad

@pytest.fixture
def mock_board():
    board = MagicMock()
    board.notes_mode = False
    board.toggle_notes_mode = MagicMock()
    return board

@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    # Use dummy video driver so pygame doesn't open a window
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def numberpad(mock_board):
    # Patch SysFont so the numberpad uses a mock font
    mock_font = MagicMock()
    mock_surface = MagicMock()
    mock_surface.get_rect.return_value = pygame.Rect(0, 0, 10, 10)
    mock_font.render.return_value = mock_surface
    with patch("pygame.font.SysFont", return_value=mock_font):
        np = NumberPad(screen_size=800, board_size=400, board=mock_board)
    return np

@pytest.fixture
def mock_screen():
    return MagicMock()

def test_numberpad_initialization(numberpad):
    # Check buttons and switch_rect exist
    assert len(numberpad.buttons) == 9
    assert hasattr(numberpad, "switch_rect")
    assert hasattr(numberpad, "mode_label_font")

def test_draw_calls_methods(numberpad, mock_screen):
    np = numberpad

    # Patch pygame.draw functions to avoid real rendering
    with patch("pygame.draw.circle"), patch("pygame.draw.rect"), patch("pygame.draw.polygon"):
        np.draw(mock_screen)

    # Ensure screen.blit is called at least once for text
    assert mock_screen.blit.called

def test_handle_event_number_button(numberpad):
    np = numberpad
    # Pick the first button's position
    x, y = np.buttons[0][1]
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(x, y))
    result = np.handle_event(event)
    assert result == 1  # first button

def test_handle_event_toggle_switch(numberpad, mock_board):
    np = numberpad
    # Click inside the switch_rect
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=np.switch_rect.center)
    np.handle_event(event)
    mock_board.toggle_notes_mode.assert_called_once()

def test_handle_event_no_action(numberpad):
    np = numberpad
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(0, 0))  # outside any button
    result = np.handle_event(event)
    assert result is None
