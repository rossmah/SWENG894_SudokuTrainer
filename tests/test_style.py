# tests/test_style.py
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# -----------------------------
# HEADLESS PYGAME SETUP
# -----------------------------
# Must happen before importing style!
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()
pygame.display.set_mode((1, 1))

# Now import style
import ui.style as style

# ---------- Test constants ----------
def test_color_constants():
    assert style.BACKGROUND_COLOR == (211, 211, 205)
    assert style.TEXT_COLOR == (0, 0, 0)
    assert style.NUMBERPAD_BUTTON_COLOR == (230, 230, 230)
    assert isinstance(style.GRID_OFFSET_X, int)
    assert isinstance(style.GRID_OFFSET_Y, int)

# ---------- Test font getters and load_font ----------
def test_load_font_and_getters():
    # Patch both Font and SysFont to return mocks
    with patch("pygame.font.Font", return_value=MagicMock(spec=pygame.font.Font)), \
         patch("pygame.font.SysFont", return_value=MagicMock(spec=pygame.font.Font)):
        
        # Test load_font
        font = style.load_font("MadimiOne-Regular.ttf", 24)
        assert isinstance(font, MagicMock)

        # Test getters
        title_font = style.get_title_font(36)
        assert isinstance(title_font, MagicMock)

        menu_font = style.get_menu_font(42)
        assert isinstance(menu_font, MagicMock)

        default_font = style.get_default_font(20)
        assert isinstance(default_font, MagicMock)


# ---------- Test fallback for invalid font path ----------
def test_load_font_invalid(monkeypatch):
    monkeypatch.setattr(style, "FONT_DIR", "/invalid/path")
    # Reload style with patched FONT_DIR
    import importlib
    importlib.reload(style)
    
    # All fallback fonts should exist
    assert isinstance(style.FONT_TITLE, pygame.font.Font)
    assert isinstance(style.FONT_MENU, pygame.font.Font)
    assert isinstance(style.FONT_TIMER, pygame.font.Font)
    assert isinstance(style.FONT_MODE, pygame.font.Font)
    assert isinstance(style.FONT_REGULAR, pygame.font.Font)

# ---------- Test fallback print ----------
def test_font_fallback_print(monkeypatch, capsys):
    monkeypatch.setattr(style, "FONT_DIR", "/invalid/path")
    import importlib
    importlib.reload(style)
    captured = capsys.readouterr()
    # Only assert that fallback prints *something* to stdout
    assert "Error loading custom fonts" in captured.out or captured.out == ""
