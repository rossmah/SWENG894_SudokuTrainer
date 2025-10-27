# src/hints/heuristics/naked_singles.py 
from hints.utils.board_utils import *

# Naked Singles Heuristic
# -----------------------
# A 'naked single' occurs when a cell has only one possible value
# based on Sudoku constraints (row, column, block).
# This function identifies all such cells on the board
# -----------------------

#
# Find all naked singles on the board
#
# Args:
#    board (Board): The current game board instance
#
# Returns:
#    list[dict]: A list of hints. Each hint dictionary contains:
#        {
#            'technique': 'Naked Single',
#            'cell': (row, col),
#            'value': int,
#            'reason': 'Only possible number for this cell'
#            'where': list[str]
#        }
#
def find_naked_singles(board):
    hints = []

    for r in range(board.size):
        for c in range(board.size):
            if board.user_board[r][c] == 0:  # Only check cells without a final value
                candidates = get_candidates_for_cell(board, r, c)
                if len(candidates) == 1:
                    val = next(iter(candidates))
                    ui_cell = cell_to_ui_cell([(r, c)])[0]
                    hints.append({
                        'technique': 'Naked Single',
                        'cell': (r, c),
                        'value': val,
                        'reason': f'Cell {ui_cell} can only be {val}.',
                        'where': ['cell']
                    })

    return hints
