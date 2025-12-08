# tests/test_save_load.py
import os
import json
import pytest
from unittest.mock import MagicMock, patch
from ui.save_load import save_game, load_game, SAVE_PATH
from ui.board import Board
from ui.timer import Timer


# -----------------------------
# TC-14.1-PersistCurrentGameToFile
# -----------------------------
def test_persist_current_game_to_file(tmp_path):
    # Arrange
    board = MagicMock()
    board.user_board = [[0]*9 for _ in range(9)]
    board.givens = [[False]*9 for _ in range(9)]
    board.locked = [[False]*9 for _ in range(9)]
    board.notes = [[set() for _ in range(9)] for _ in range(9)]
    board.solution = [[0]*9 for _ in range(9)]
    
    timer = MagicMock()
    timer.get_elapsed.return_value = 42.0
    
    difficulty = "Medium"

    # Redirect SAVE_PATH to tmp directory
    with patch("ui.save_load.SAVE_PATH", tmp_path / "saved_game.json"):
        # Act
        save_game(board, timer, difficulty)

        # Assert
        assert (tmp_path / "saved_game.json").exists()
        with open(tmp_path / "saved_game.json", "r") as f:
            data = json.load(f)
        assert data["board"]["user_board"] == board.user_board
        assert data["timer"]["elapsed_time"] == 42.0
        assert data["difficulty"] == difficulty

# -----------------------------
# TC-14.2-ReloadSavedGame
# -----------------------------
def test_load_game_reconstructs_board(tmp_path):
    # Arrange
    save_data = {
        "board": {
            "user_board": [[1]*9 for _ in range(9)],
            "givens": [[True]*9 for _ in range(9)],
            "locked": [[True]*9 for _ in range(9)],
            "notes": [[[] for _ in range(9)] for _ in range(9)],
            "solution": [[1]*9 for _ in range(9)]
        },
        "timer": {"elapsed_time": 10.0},
        "difficulty": "Easy"
    }
    save_file = tmp_path / "saved_game.json"
    with open(save_file, "w") as f:
        json.dump(save_data, f)

    # Patch SAVE_PATH to tmp file
    with patch("ui.save_load.SAVE_PATH", save_file):
        # Act
        board, timer, numberpad, sidebar, difficulty = load_game(None, 9, 800)

        # Assert
        assert board is not None
        assert timer is not None
        assert difficulty == "Easy"
        assert board.user_board[0][0] == 1
        assert board.givens[0][0] is True
        assert board.locked[0][0] is True

# -----------------------------
# TC-14.3-RestoreTimerfromSave
# -----------------------------
def test_load_game_restores_timer(tmp_path):
    # Arrange
    save_data = {
        "board": {
            "user_board": [[0]*9 for _ in range(9)],
            "givens": [[False]*9 for _ in range(9)],
            "locked": [[False]*9 for _ in range(9)],
            "notes": [[[] for _ in range(9)] for _ in range(9)],
            "solution": [[0]*9 for _ in range(9)]
        },
        "timer": {"elapsed_time": 123.45},
        "difficulty": "Hard"
    }
    save_file = tmp_path / "saved_game.json"
    with open(save_file, "w") as f:
        json.dump(save_data, f)

    with patch("ui.save_load.SAVE_PATH", save_file):
        # Act
        board, timer, numberpad, sidebar, difficulty = load_game(None, 9, 800)

        # Assert
        assert timer.elapsed_time >= 123.45

def test_save_game_with_none_inputs(tmp_path):
    with patch("ui.save_load.SAVE_PATH", tmp_path / "dummy.json"):
        # Should not raise an exception even if board or timer is None
        save_game(None, None, "Easy")
        save_game(MagicMock(), None, "Medium")
        save_game(None, MagicMock(), "Hard")

def test_save_game_write_error(monkeypatch):
    board = MagicMock()
    timer = MagicMock()
    timer.get_elapsed.return_value = 0.0

    def fake_open(*args, **kwargs):
        raise IOError("Cannot write file")

    monkeypatch.setattr("builtins.open", fake_open)

    # Should not raise exception
    save_game(board, timer, "Easy")
