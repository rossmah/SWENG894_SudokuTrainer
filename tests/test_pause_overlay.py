# tests/test_pause_overlay.py
import pygame
import pytest
from ui.pause_overlay import PauseOverlay
import ui.style as style

pygame.init()

@pytest.fixture
def overlay():
    return PauseOverlay()

def test_init(overlay):
    assert overlay.active is False
    assert overlay.buttons == []

def test_add_button(overlay):
    rect = overlay.add_button("Resume", 10, 20, 100, 50)
    assert isinstance(rect, pygame.Rect)
    assert len(overlay.buttons) == 1
    assert overlay.buttons[0][1] == "Resume"
    # Check rect coordinates
    assert rect.x == 10
    assert rect.y == 20
    assert rect.width == 100
    assert rect.height == 50

def test_handle_event_click_inside(overlay):
    overlay.add_button("Resume", 0, 0, 50, 50)
    # Click inside button
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(25, 25))
    result = overlay.handle_event(event)
    assert result == "resume"

def test_handle_event_click_outside(overlay):
    overlay.add_button("Resume", 0, 0, 50, 50)
    # Click outside button
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(100, 100))
    assert overlay.handle_event(event) is None

def test_handle_event_wrong_type(overlay):
    overlay.add_button("Resume", 0, 0, 50, 50)
    # Non-MOUSEBUTTONUP event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
    assert overlay.handle_event(event) is None

def test_draw_execution(overlay):
    # Create a minimal surface
    screen = pygame.Surface((200, 200))
    overlay.add_button("Resume", 50, 50, 100, 40)
    
    # Call draw; should run without errors
    overlay.draw(screen, 200, 200, "12:34")

def test_multiple_buttons_draw(overlay):
    screen = pygame.Surface((300, 300))
    overlay.add_button("Resume", 10, 10, 80, 30)
    overlay.add_button("Menu", 10, 50, 80, 30)
    overlay.draw(screen, 300, 300, "05:12")
    assert len(overlay.buttons) == 2

def test_active_flag_behavior():
    ov = PauseOverlay()
    ov.active = True
    assert ov.active
    ov.active = False
    assert not ov.active

def test_add_button_multiple(overlay):
    overlay.add_button("Resume", 0, 0, 50, 50)
    overlay.add_button("Menu", 60, 0, 50, 50)
    assert len(overlay.buttons) == 2
    labels = [b[1] for b in overlay.buttons]
    assert "Resume" in labels
    assert "Menu" in labels
