# tests/test_board_conflicts.py
import pytest
from ui.board import Board

@pytest.fixture
def empty_board():
    return Board(size=9)

@pytest.fixture
def notes_board():
    board = Board(size=9)
    board.notes_mode = True
    board.selected_cell = (0, 0)
    return board

@pytest.fixture
def board():
    b = Board(size=9)
    b.selected_cell = (0, 0)  # select top-left cell for testing
    return b

# ----- US-8: CONFLICT HIGHLIGHTING -------
def test_row_conflict_detection(empty_board):
    # TC-8.1: Row Conflict Detection
    board = empty_board
    # Place two 5's in the same row
    board.user_board[0][0] = 5
    board.user_board[0][5] = 5
    conflicts = board.get_conflicts(0, 0)
    
    assert (0, 5) in conflicts
    assert len(conflicts) == 1

def test_column_conflict_detection(empty_board):
    # TC-8.2: Column Conflict Detection
    board = empty_board
    # Place two 5's in the same column
    board.user_board[0][0] = 5
    board.user_board[6][0] = 5
    conflicts = board.get_conflicts(0, 0)
    
    assert (6, 0) in conflicts
    assert len(conflicts) == 1

def test_block_conflict_detection(empty_board):
    # TC-8.3: Block Conflict Detection
    board = empty_board
    # Place two 5's in the same 3x3 block
    board.user_board[0][0] = 5
    board.user_board[1][1] = 5
    conflicts = board.get_conflicts(0, 0)
    
    assert (1, 1) in conflicts
    assert len(conflicts) == 1

# ------ US-9: PENCIL MARKS ----
def test_add_pencil_marks(notes_board):
    # TC-9.1: Add Pencil Marks
    # Verify that multiple candidates can be added to a cell
    b = notes_board
    b.handle_number_entry(1)
    b.handle_number_entry(3)

    assert b.notes[0][0] == {1, 3}
    assert b.user_board[0][0] == 0  # no number placed


def test_remove_pencil_mark(notes_board):
    # TC-9.2: Remove Pencil Marks
    # Verify that a candidate number can be removed from a cell
    b = notes_board
    b.handle_number_entry(1)
    b.handle_number_entry(3)
    b.handle_number_entry(1)  # removes 1

    assert b.notes[0][0] == {3}


def test_given_cell_no_pencil_marks():
    # TC-9.3: Given cell no pencil marks
    # Verify that pencil marks cannot be added to a given cell
    b = Board(size=9)
    b.notes_mode = True
    b.grid[0][0] = 5
    b.user_board[0][0] = 5
    b.givens[0][0] = 1  # mark as given
    b.selected_cell = (0, 0)
    b.handle_number_entry(2)

    assert b.notes[0][0] == set()
    assert b.user_board[0][0] == 5  # given value untouched

#------ US-10: NOTES/SOLVE MODE TOGGLE -----
def test_toggle_to_notes_mode(board):
    #TC-10.1: Verify switching from Solve mode to Notes mode retains entry
    # Initially in Solve mode
    assert board.notes_mode is False

    # Toggle to Notes mode
    board.toggle_notes_mode()
    assert board.notes_mode is True

    # Enter '1' as a candidate in Notes mode
    board.handle_number_entry(1)
    assert board.notes[0][0] == {1}
    assert board.user_board[0][0] == 0  # no final value

    # Toggle back to Solve mode
    board.toggle_notes_mode()
    assert board.notes_mode is False

    # Candidate should still be retained
    assert board.notes[0][0] == {1}
    assert board.user_board[0][0] == 0

def test_toggle_to_solve_mode(board):
    #TC-10.2: Verify switching from Notes mode to Solve mode changes input behavior
    # Start in Notes mode
    board.toggle_notes_mode()
    assert board.notes_mode is True

    # Select a cell and enter '1' in Solve mode after toggling
    board.toggle_notes_mode()  # switch to Solve mode
    assert board.notes_mode is False

    # Enter '1' as a final number
    board.handle_number_entry(1)
    assert board.user_board[0][0] == 1
    assert board.notes[0][0] == set()  # candidate should not appear as final number overwrites notes

def test_toggle_multiple_times_retains_data(board):
    #TC-10.3: Verify multiple toggles retain notes and final numbers correctly
    # Toggle to Notes mode
    board.toggle_notes_mode()
    assert board.notes_mode is True

    # Enter candidate '1'
    board.handle_number_entry(1)
    assert board.notes[0][0] == {1}

    # Toggle to Solve mode
    board.toggle_notes_mode()
    assert board.notes_mode is False

    # Enter final number '3'
    board.handle_number_entry(3)
    assert board.user_board[0][0] == 3
    # Notes should remain unchanged
    assert board.notes[0][0] == {1}

    # Toggle back to Notes mode
    board.toggle_notes_mode()
    assert board.notes_mode is True
    # Candidate should still be there
    assert board.notes[0][0] == {1}
    # Final value in Solve mode should remain
    assert board.user_board[0][0] == 3