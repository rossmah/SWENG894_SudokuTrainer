# tests/test_puzzle_completion.py
import pytest
import pygame
from ui.complete_popup import CompletePopup
from ui.board import Board

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ---------------- TC-15.1: Detect Board Completion ----------------
def test_detect_board_completion():
    #Verify that when every cell is filled correctly, the board is flagged as complete.
    # --- Setup: create a nearly-complete puzzle ---
    solution = [
        [5,3,4,6,7,8,9,1,2],
        [6,7,2,1,9,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,0],  # last cell empty
    ]

    user_board = [row[:] for row in solution]
    user_board[8][8] = 0  # last cell empty

    # --- Initialize Board ---
    board = Board(puzzle=user_board, solution=solution, size=9)
    board.completed = False  # initialize completed flag

    # --- Action: fill last cell correctly ---
    board.user_board[8][8] = solution[8][8]

    # --- Validate completion ---
    completed = board.is_board_complete()
    assert completed is True
    assert board.completed is True

# ---------------- TC-15.2: Reject Board Completion ----------------
def test_reject_board_completion():
    solution = [[(c+1 + r*3)%9 + 1 for c in range(9)] for r in range(9)]
    user_board = [row[:] for row in solution]
    user_board[8][8] = 0  # last cell empty

    board = Board(puzzle=user_board, size=9, screen_size=600)
    board.solution = solution
    board.completed = False

    # Fill last cell incorrectly
    board.user_board[8][8] = (solution[8][8] % 9) + 1  # wrong value

    # Check conflicts
    conflicts = [board.get_conflicts(r, c) for r in range(9) for c in range(9) if board.user_board[r][c] != 0]
    assert any(len(c) > 0 for c in conflicts)  # at least one conflict

    # Check completion
    assert board.is_board_complete() is False
    assert board.completed is False

# ---------------- TC-15.3: Trigger Completion Popup ----------------
def test_trigger_completion_popup():
    solution = [[(c+1 + r*3)%9 + 1 for c in range(9)] for r in range(9)]
    user_board = [row[:] for row in solution]
    user_board[8][8] = 0

    board = Board(puzzle=user_board, size=9, screen_size=600)
    board.solution = solution
    board.completed = False

    # Fill last cell correctly
    board.user_board[8][8] = solution[8][8]

    # Confirm completion
    assert board.is_board_complete() is True
    assert board.completed is True

    # Initialize popup
    popup = CompletePopup(time_seconds=123, difficulty="Easy", screen_width=800, screen_height=600)
    assert popup.active is True

    # Simulate click on MAIN MENU button
    fake_event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=popup.button_rect.center)
    result = popup.handle_event(fake_event)
    assert result == "menu"
    assert popup.active is False

# --------------------------
# Test Initialization & format_time
# --------------------------
def test_init_attributes():
    popup = CompletePopup(123, "Medium", SCREEN_WIDTH, SCREEN_HEIGHT)
    assert popup.time_seconds == 123
    assert popup.difficulty == "Medium"
    assert popup.screen_width == SCREEN_WIDTH
    assert popup.screen_height == SCREEN_HEIGHT
    assert popup.active is True
    assert hasattr(popup, "card_rect")
    assert hasattr(popup, "button_rect")

def test_format_time():
    # 0 seconds
    popup = CompletePopup(0, "Easy", SCREEN_WIDTH, SCREEN_HEIGHT)
    assert popup.format_time() == "00:00"

    # 65 seconds -> 01:05
    popup = CompletePopup(65, "Easy", SCREEN_WIDTH, SCREEN_HEIGHT)
    assert popup.format_time() == "01:05"

    # 3605 seconds -> 60:05
    popup = CompletePopup(3605, "Easy", SCREEN_WIDTH, SCREEN_HEIGHT)
    assert popup.format_time() == "60:05"

# --------------------------
# Test draw method
# --------------------------
def test_draw_active_runs_without_error():
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    popup = CompletePopup(123, "Hard", SCREEN_WIDTH, SCREEN_HEIGHT)
    popup.draw(screen)  # should not raise any exceptions

def test_draw_inactive_does_nothing():
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    popup = CompletePopup(123, "Hard", SCREEN_WIDTH, SCREEN_HEIGHT)
    popup.active = False
    popup.draw(screen)  # should not raise, should skip drawing

# --------------------------
# Test handle_event
# --------------------------
def test_handle_event_click_button():
    popup = CompletePopup(123, "Easy", SCREEN_WIDTH, SCREEN_HEIGHT)
    event = pygame.event.Event(
        pygame.MOUSEBUTTONUP,
        pos=(popup.button_rect.centerx, popup.button_rect.centery)
    )
    result = popup.handle_event(event)
    assert result == 'menu'
    assert popup.active is False

def test_handle_event_click_outside_returns_none():
    popup = CompletePopup(123, "Easy", SCREEN_WIDTH, SCREEN_HEIGHT)
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(0, 0))
    assert popup.handle_event(event) is None
    # active should remain True
    assert popup.active is True

def test_handle_event_inactive_returns_none():
    popup = CompletePopup(123, "Easy", SCREEN_WIDTH, SCREEN_HEIGHT)
    popup.active = False
    event = pygame.event.Event(
        pygame.MOUSEBUTTONUP,
        pos=(popup.button_rect.centerx, popup.button_rect.centery)
    )
    assert popup.handle_event(event) is None
    assert popup.active is False

# --------------------------
# Optional: test different screen sizes
# --------------------------
@pytest.mark.parametrize("width,height", [(400, 300), (1920, 1080), (600, 600)])
def test_draw_various_screen_sizes(width, height):
    screen = pygame.Surface((width, height))
    popup = CompletePopup(90, "Easy", width, height)
    popup.draw(screen)  # should run without exception