import pytest
from unittest.mock import MagicMock, patch
import pygame
from ui.menu import Menu

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def dummy_items():
    return [("Easy", "easy_action"), ("Medium", "medium_action"), ("Hard", "hard_action")]

@pytest.fixture
def dummy_font(init_pygame):
    # Use a real Pygame font to avoid font errors
    return pygame.font.SysFont("arial", 24)

@pytest.fixture
def dummy_screen(init_pygame):
    # Use a real surface for drawing
    return pygame.Surface((800, 600))

def test_menu_initialization(dummy_items, dummy_font):
    with patch("ui.style.get_title_font", return_value=dummy_font), \
         patch("ui.style.get_default_font", return_value=dummy_font):
        menu = Menu(dummy_items, dummy_font, x=100, y=100, menu_type='DIFFICULTY')
        assert menu.items == dummy_items
        assert menu.menu_type == 'DIFFICULTY'
        assert len(menu.buttons) == len(dummy_items)

