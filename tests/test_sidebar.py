import pytest
import pygame
from unittest.mock import MagicMock, patch
from ui.sidebar import Sidebar
import ui.style as style

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# Fixture for mocked dependencies
@pytest.fixture
def sidebar_mocks():
    board = MagicMock()
    board.screen_size = 400
    numberpad = MagicMock()
    timer = MagicMock()
    timer.paused = False
    screen_width = 800
    return board, numberpad, timer, screen_width

def test_sidebar_initialization(sidebar_mocks):
    board, numberpad, timer, screen_width = sidebar_mocks
    with patch("ui.style.get_title_font") as mock_font:
        mock_font.return_value = MagicMock()
        mock_font.return_value.render.return_value.get_rect.return_value = pygame.Rect(0, 0, 100, 30)
        sidebar = Sidebar(board, numberpad, timer, screen_width)
        assert hasattr(sidebar, "title_surface")
        assert hasattr(sidebar, "title_rect")
        assert sidebar.board == board
        assert sidebar.numberpad == numberpad
        assert sidebar.timer == timer

def test_draw_calls_blit(sidebar_mocks):
    board, numberpad, timer, screen_width = sidebar_mocks
    sidebar = Sidebar(board, numberpad, timer, screen_width)

    mock_screen = MagicMock()  # mock screen with blit
    with patch("ui.style.get_title_font") as mock_font:
        mock_font.return_value = MagicMock()
        mock_font.return_value.render.return_value = MagicMock()
        sidebar.draw(mock_screen)

    # Should call blit at least once for title
    assert mock_screen.blit.call_count >= 1
    timer.draw.assert_called()
    numberpad.draw.assert_called()

def test_draw_after_timer_paused(sidebar_mocks):
    board, numberpad, timer, screen_width = sidebar_mocks
    timer.paused = True
    sidebar = Sidebar(board, numberpad, timer, screen_width)

    mock_screen = MagicMock()
    with patch("ui.style.get_title_font") as mock_font:
        mock_font.return_value = MagicMock()
        mock_font.return_value.render.return_value = MagicMock()
        sidebar.draw(mock_screen)

    numberpad.draw.assert_not_called()
    timer.draw.assert_called()
