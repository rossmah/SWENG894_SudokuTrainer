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

def test_locked_cell_ignored(board):
    board.locked[0][0] = 1
    board.handle_number_entry(5)
    assert board.user_board[0][0] == 0

def test_delete_number_clears_cell(board):
    board.user_board[0][0] = 5
    board.handle_number_entry(0)
    assert board.user_board[0][0] == 0

def test_handle_import_entry_places_and_clears_notes():
    board = Board(size=9, import_mode=True)
    board.notes[0][0].add(3)
    board.selected_cell = (0, 0)
    board.handle_import_entry(5)
    assert board.user_board[0][0] == 5
    assert board.grid[0][0] == 5
    assert board.notes[0][0] == set()

def test_handle_import_entry_removes_number():
    board = Board(size=9, import_mode=True)
    board.user_board[0][0] = 5
    board.selected_cell = (0, 0)
    board.handle_import_entry(0)
    assert board.user_board[0][0] == 0

def test_highlight_cells_single_cell():
    board = Board(size=9)
    board.selected_cell = (0, 0)

    # Hint targeting cell (1,1) with value 5 (1-based UI coordinates)
    hint = {'cell': (1, 1), 'value': 5}
    board.highlight_cells([hint])

    # Internally converted to 0-based indices -> (0,0)
    assert (0, 0) in board.highlighted_candidates
    assert board.highlighted_candidates[(0, 0)] == {5}

def test_highlight_eliminations_multiple(board):
    elim = {'cell': [(1,1),(2,2)], 'remove': [3,4]}
    board.highlight_eliminations([elim])
    assert board.highlighted_eliminations[(0,0)] == {3,4}
    assert board.highlighted_eliminations[(1,1)] == {3,4}

def test_reset_to_givens(board):
    board.user_board[0][0] = 5
    board.notes[0][0].add(1)
    board.highlighted_candidates[(0,0)] = {1}
    board.reset_to_givens()
    assert board.user_board[0][0] == 0
    assert board.notes[0][0] == set()
    assert board.highlighted_candidates == {}

def test_is_board_complete_true():
    solution = [[1]*9 for _ in range(9)]
    board = Board(size=9, solution=solution)
    board.user_board = [row[:] for row in solution]
    assert board.is_board_complete() is True

def test_is_board_complete_false():
    solution = [[1]*9 for _ in range(9)]
    board = Board(size=9, solution=solution)
    board.user_board[0][0] = 2
    assert board.is_board_complete() is False

def test_is_board_complete_no_solution():
    board = Board(size=9)
    assert board.is_board_complete() is False

def test_number_count_limit_max_reached(board):
    board.selected_cell = (0, 1)
    for i in range(9):
        board.user_board[i][0] = 1
    board.handle_number_entry(1)
    # Number is still placed in the selected cell
    assert board.user_board[0][1] == 1

def test_number_count_limit_not_full(board):
    # Only 8 of number '2' exist
    for r in range(8):
        board.user_board[r][0] = 2
    board.update_number_counts()

    board.selected_cell = (8, 1)
    board.handle_number_entry(2)  # should allow placement
    assert board.user_board[8][1] == 2

def test_invalid_number_entry_negative(board):
    board.selected_cell = (0, 0)
    board.handle_number_entry(-1)
    assert board.user_board[0][0] == -1

def test_invalid_number_entry_too_high(board):
    board.selected_cell = (0, 0)
    board.handle_number_entry(10)
    assert board.user_board[0][0] == 10

def test_conflicts_multiple_sources(empty_board):
    board = Board(size=9)
    # Place same number in row, column, and block
    board.user_board[0][0] = 5
    board.user_board[0][1] = 5  # same row
    board.user_board[1][0] = 5  # same column
    board.user_board[1][1] = 5  # same block
    conflicts = board.get_conflicts(0, 0)
    assert set(conflicts) == {(0,1), (1,0), (1,1)}

def test_highlight_cells_empty_input(board):
    board.highlighted_candidates = {}
    board.highlight_cells([])
    assert board.highlighted_candidates == {}

def test_highlight_eliminations_empty_input(board):
    board.highlighted_eliminations = {}
    board.highlight_eliminations([])
    assert board.highlighted_eliminations == {}

def test_notes_mode_add_remove_multiple_cells(notes_board):
    b = notes_board
    # Add notes to two different cells
    b.selected_cell = (0, 0)
    b.handle_number_entry(1)
    b.selected_cell = (0, 1)
    b.handle_number_entry(2)
    assert b.notes[0][0] == {1}
    assert b.notes[0][1] == {2}

def test_switch_notes_does_not_clear_final(board):
    board.toggle_notes_mode()  # Notes mode
    board.handle_number_entry(1)
    board.toggle_notes_mode()  # Solve mode
    board.handle_number_entry(3)
    assert board.user_board[0][0] == 3
    # Notes remain
    assert board.notes[0][0] == {1}

def test_reset_highlights_after_reset(board):
    board.highlighted_candidates[(0,0)] = {1}
    board.highlighted_eliminations[(1,1)] = {2}
    board.reset_to_givens()
    assert board.highlighted_candidates == {}
    assert board.highlighted_eliminations == {}
