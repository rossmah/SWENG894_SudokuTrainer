import time
import pytest
import pygame
from unittest.mock import MagicMock, patch
from ui.timer import Timer

def test_timer_start(monkeypatch):
    # Arrange
    timer = Timer(font=None, x=0, y=0)
    fake_time = [100.0]  # simulated time
    monkeypatch.setattr(time, "time", lambda: fake_time[0])

    # Act
    timer.start()  # starts timer at 100.0
    fake_time[0] = 105.0  # advance simulated time by 5 seconds
    elapsed = timer.get_elapsed()

    # Assert
    assert elapsed == pytest.approx(5.0, rel=1e-2)
    assert timer.start_time == 100.0
    assert not timer.paused

def test_timer_pause(monkeypatch):
    # Arrange
    timer = Timer(font=None, x=0, y=0)
    fake_time = [200.0]
    monkeypatch.setattr(time, "time", lambda: fake_time[0])
    timer.start()  # start at 200

    # Simulate elapsed time
    fake_time[0] = 210.0
    timer.pause()  # pause at 210
    first_check = timer.get_elapsed()

    # Wait 5 simulated seconds
    fake_time[0] = 215.0
    second_check = timer.get_elapsed()

    # Assert (paused, so no change)
    assert first_check == pytest.approx(second_check, rel=1e-2)
    assert timer.paused

def test_timer_resume(monkeypatch):
    # Arrange
    timer = Timer(font=None, x=0, y=0)
    fake_time = [300.0]
    monkeypatch.setattr(time, "time", lambda: fake_time[0])
    timer.start()  # start at 300

    # Let 10 seconds pass
    fake_time[0] = 310.0
    timer.pause()  # pause at 310
    paused_elapsed = timer.get_elapsed()

    # Wait while paused (shouldn’t count)
    fake_time[0] = 320.0
    timer.resume()  # resume at 320

    # Wait 5 more seconds after resuming
    fake_time[0] = 325.0
    resumed_elapsed = timer.get_elapsed()

    # Assert
    assert resumed_elapsed > paused_elapsed
    assert resumed_elapsed == pytest.approx(15.0, rel=1e-2)
    assert not timer.paused



def test_timer_toggle(monkeypatch):
    timer = Timer(font=None, x=0, y=0)
    fake_time = [100]
    monkeypatch.setattr(time, "time", lambda: fake_time[0])
    
    # Toggle when paused = False -> should pause
    timer.start()
    timer.toggle()
    assert timer.paused
    pause_start = timer.pause_start
    
    # Toggle again -> should resume
    fake_time[0] += 5
    timer.toggle()
    assert not timer.paused
    assert timer.total_paused == 5.0

def test_timer_draw_and_resume_button(monkeypatch):
    timer = Timer(font=MagicMock(), x=0, y=0)
    
    # Patch pygame functions to avoid real rendering
    with patch("pygame.Surface", MagicMock()), patch("pygame.draw.rect"), patch("pygame.font.Font", MagicMock()), \
         patch("pygame.font.SysFont", MagicMock()), patch("pygame.display.set_mode", MagicMock()):
        screen = MagicMock()
        
        # Draw when not paused (pause bars)
        timer.start_time = 0
        timer.paused = False
        timer.draw(screen, 200, 200, timer.font)
        
        # Draw when paused (overlay + resume button)
        timer.paused = True
        timer.resume_rect = None  # simulate first draw
        timer.draw(screen, 200, 200, timer.font)
        assert timer.resume_rect is not None

def test_handle_event(monkeypatch):
    timer = Timer(font=None, x=0, y=0)
    fake_pos = (5, 5)
    event = MagicMock(type=pygame.MOUSEBUTTONUP, pos=fake_pos)
    
    # Set up pause_rect to collide
    timer.pause_rect = pygame.Rect(0,0,10,10)
    timer.paused = False
    handled = timer.handle_event(event)
    assert handled
    assert timer.paused  # toggled pause

    # Resume button case
    timer.resume_rect = pygame.Rect(0,0,10,10)
    timer.paused = True
    handled = timer.handle_event(event)
    assert handled
    assert not timer.paused  # toggled resume

def test_get_elapsed_before_start():
    timer = Timer(font=None, x=0, y=0)
    assert timer.get_elapsed() == 0
