# tests/test_restart_puzzle.py
import pytest
from ui.board import Board
from ui.timer import Timer
import pygame

@pytest.fixture
def sample_board():
    board = Board()
    # Fill in some givens
    board.grid[0][0] = 5
    board.grid[1][1] = 3
    board.user_board = [row[:] for row in board.grid]
    board.givens = [[1 if cell != 0 else 0 for cell in row] for row in board.grid]
    # Add some user entries
    board.user_board[0][1] = 7
    board.user_board[2][2] = 9
    # Add notes
    board.notes[0][2].add(1)
    board.notes[1][0].add(2)
    return board

@pytest.fixture
def sample_timer():
    pygame.init()
    font = pygame.font.SysFont("arial", 24)
    timer = Timer(font, x=0, y=0)
    timer.elapsed_time = 42  # simulate timer > 0
    timer.start()
    return timer

# ------------------- US-5: Restart Puzzle -------------------

# UT TC-5.1: Reset Board - verify all non-given cells are cleared, givens remain
def test_reset_board(sample_board):
    board = sample_board
    # Make a copy of original puzzle
    original_user_board = [row[:] for row in board.grid]

    # Call reset_to_givens
    board.reset_to_givens()

    # Verify board state
    for r in range(9):
        for c in range(9):
            if board.givens[r][c]:
                assert board.user_board[r][c] == board.grid[r][c]  # givens preserved
            else:
                assert board.user_board[r][c] == 0  # user entries cleared

# UT TC-5.2: Reset Notes - verify all notes and candidate highlights are cleared
def test_reset_notes(sample_board):
    board = sample_board
    # Add additional highlights for testing
    board.highlighted_candidates[(0,2)] = {1}
    board.highlighted_eliminations[(1,0)] = {2}

    # Reset board
    board.reset_to_givens()

    # Notes cleared
    for r in range(9):
        for c in range(9):
            assert board.notes[r][c] == set()

    # Highlights cleared
    assert board.highlighted_candidates == {}
    assert board.highlighted_eliminations == {}

# UT TC-5.3: Reset Timer - verify timer and progress tracking reset
def test_reset_timer(sample_timer):
    timer = sample_timer
    # Simulate some elapsed time
    elapsed_before = timer.get_elapsed()
    assert elapsed_before > 0

    # Restart timer
    timer.restart()

    # Verify timer reset
    assert timer.get_elapsed() < 1  # Allow slight delay
    assert timer.paused is False
    assert timer.total_paused == 0
    assert timer.completed is False
