import pytest
import pygame
from unittest.mock import patch
from ui.import_menu import ImportMenu
from core import generator

# Don't allow pygame to initialize a real display in unit tests
# Avoids errors on headless test runners.
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    import pygame
    pygame.display.init()
    pygame.display.set_mode((1,1))
    yield
    pygame.display.quit()


# ------------------------------------------------------------
# TC-2.1 — Valid 9×9 puzzle should be accepted
# ------------------------------------------------------------
def test_valid_custom_puzzle_structure():
    menu = ImportMenu(800, 600)

    # A simple valid puzzle
    valid_grid = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9],
    ]

    menu.board.user_board = valid_grid

    # Mock: no conflicts anywhere
    menu.board.get_conflicts = lambda r, c: []

    # Mock the solver to simulate a successful solve
    with patch("core.generator.solve", return_value=True):
        success, solved = menu._finish_import()

    assert success is True
    assert solved is not None


# ------------------------------------------------------------
# TC-2.2 — Invalid puzzle (conflict) should be rejected
# ------------------------------------------------------------
def test_invalid_custom_puzzle_is_rejected():
    menu = ImportMenu(800, 600)

    # Duplicate "5" in row 0 - conflict
    invalid_grid = [
        [5,5,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9],
    ]

    menu.board.user_board = invalid_grid

    # Mock conflict detection: return conflict if row 0
    def get_conflicts_mock(r, c):
        return ["duplicate"] if r == 0 and c in (0,1) else []

    menu.board.get_conflicts = get_conflicts_mock

    with patch("core.generator.solve", return_value=True):
        success, solved = menu._finish_import()

    assert success is False
    assert solved is None


# ------------------------------------------------------------
# TC-2.3 — Invalid - corrected - accepted
# ------------------------------------------------------------
def test_fixed_puzzle_is_accepted_after_rejection():
    menu = ImportMenu(800, 600)

    # First: invalid puzzle (needs fixing)
    invalid_grid = [
        [5,5,0,0,7,0,0,0,0],  # duplicate 5s
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9],
    ]

    menu.board.user_board = invalid_grid
    menu.board.get_conflicts = lambda r, c: ["duplicate"] if r == 0 else []

    with patch("core.generator.solve", return_value=True):
        success1, solved1 = menu._finish_import()

    # Should fail first time
    assert success1 is False
    assert solved1 is None

    # ------------------------------------------------------
    # Fix the puzzle
    # ------------------------------------------------------
    fixed_grid = [
        [5,3,0,0,7,0,0,0,0],  # corrected row
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9],
    ]

    menu.board.user_board = fixed_grid
    menu.board.get_conflicts = lambda r, c: []  # no conflicts now

    with patch("core.generator.solve", return_value=True):
        success2, solved2 = menu._finish_import()

    assert success2 is True
    assert solved2 is not None

# Additional tests:
# ----------------------------
# 1. Mouse & Key Event Handling
# ----------------------------
def test_select_cell_and_number_entry():
    menu = ImportMenu(800, 600)
    
    # Click on cell (0,0)
    cell_pos = (menu.board.cell_size // 2, menu.board.cell_size // 2)
    menu.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': cell_pos}))
    assert menu.board.selected_cell is not None

    # Type number
    menu.board.selected_cell = (0, 0)
    menu.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_1}))
    assert menu.board.user_board[0][0] == 1

    # Delete number
    menu.handle_event(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_BACKSPACE}))
    assert menu.board.user_board[0][0] == 0

# ----------------------------
# 2. Finish Import Logic
# ----------------------------
def test_finish_import_valid_and_invalid():
    menu = ImportMenu(800, 600)
    
    # Invalid: conflict
    menu.board.user_board[0][0] = 1
    menu.board.user_board[0][1] = 1
    success, solved = menu._finish_import()
    assert not success
    assert solved is None

    # Valid: solvable board
    puzzle, solution = generator.generate_sudoku("easy")
    menu.board.user_board = [row[:] for row in puzzle]
    success, solved = menu._finish_import()
    assert success
    assert solved is not None

# ----------------------------
# 3. prepare_import_mode
# ----------------------------
def test_prepare_import_mode():
    menu = ImportMenu(800, 600)
    menu.board.prepare_import_mode()
    for row in menu.board.user_board:
        assert all(v == 0 for v in row)

# ----------------------------
# 4. finalize_import
# ----------------------------
def test_finalize_import():
    menu = ImportMenu(800, 600)
    puzzle, solution = generator.generate_sudoku("easy")
    menu.board.grid = [row[:] for row in puzzle]
    menu.board.user_board = [row[:] for row in puzzle]
    menu.board.finalize_import(solution)
    assert menu.board.import_mode is False
    # Check that all non-zero cells became givens
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != 0:
                assert menu.board.givens[r][c] == 1

# ----------------------------
# 5. reset_to_givens
# ----------------------------
def test_reset_to_givens():
    menu = ImportMenu(800, 600)
    menu.board.user_board[0][0] = 5
    menu.board.reset_to_givens()
    # Either cleared or locked as given
    assert menu.board.user_board[0][0] == 0 or menu.board.givens[0][0] == 1

# ----------------------------
# 6. Mouse click outside button
# ----------------------------
def test_mouse_click_outside_finish():
    menu = ImportMenu(800, 600)
    pos = (10, 10)
    result = menu.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos}))
    assert result is None

# ----------------------------
# 7. Draw does not crash
# ----------------------------
def test_draw():
    menu = ImportMenu(800, 600)
    surface = pygame.Surface((800, 600))
    menu.draw(surface)

# ----------------------------
# 8. Integration: import - fix conflicts - approve
# ----------------------------
def test_import_fix_conflict_and_approve():
    menu = ImportMenu(800, 600)
    menu.board.user_board[0][0] = 1
    menu.board.user_board[0][1] = 1
    success, solved = menu._finish_import()
    assert not success

    menu.board.user_board[0][1] = 2
    success, solved = menu._finish_import()
    assert success
    assert solved is not None

# ----------------------------
# 9. Notify update coverage
# ----------------------------
def test_notify_update_listener():
    menu = ImportMenu(800, 600)
    called = {"flag": False}
    def listener():
        called["flag"] = True
    menu.board.register_update_listener(listener)
    menu.board._notify_update()
    assert called["flag"] is True