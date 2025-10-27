# src/hints/utils/board_utils.py

# Common helper functions used by Sudoku heuristics

# Helper to format reason with 1-indexed positions
def cell_to_ui_cell(cells):
    return [(r + 1, c + 1) for r, c in cells]

def get_block_bounds(row: int, col: int, block_size: int = 3):
    # Return start/end indices for the 3x3 block containing (row, col)
    r0 = (row // block_size) * block_size
    c0 = (col // block_size) * block_size
    return r0, r0 + block_size, c0, c0 + block_size

def get_block_values(board, row: int, col: int):
    # Return the set of values present in the 3x3 block for a given cell
    r0, r1, c0, c1 = get_block_bounds(row, col)
    values = set()
    for rr in range(r0, r1):
        for cc in range(c0, c1):
            val = board.user_board[rr][cc]
            if val != 0:
                values.add(val)
    return values

def get_row_values(board, row: int):
    # Return the set of nonzero values in a given row
    return {v for v in board.user_board[row] if v != 0}

def get_col_values(board, col: int):
    # Return the set of nonzero values in a given column
    return {board.user_board[r][col] for r in range(board.size) if board.user_board[r][col] != 0}

def get_candidates_for_cell(board, row: int, col: int):
    # Return the set of legal candidates for a given empty cell 
    if board.user_board[row][col] != 0:
        return set()  # already filled

    used = (
        get_row_values(board, row)
        | get_col_values(board, col)
        | get_block_values(board, row, col)
    )
    return set(range(1, 10)) - used

#
# Return a 9x9 list of sets of candidates for each empty cell
# Already filled cells have an empty set
#
def get_all_candidates(board):
    size = board.size
    candidates = [[set() for _ in range(size)] for _ in range(size)]
    for r in range(size):
        for c in range(size):
            candidates[r][c] = get_candidates_for_cell(board, r, c)
    return candidates

# Nicely print a list of hints to the console. Used for testing
#
# Args:
#    findings (list[dict]): List of hint dictionaries returned by heuristics
#
def pretty_print_findings(findings):
    if not findings:
        print("No hints found.")
        return

    print("=== Hints Found ===")
    for hint in findings:
        print(f"{hint['technique']}: Cell {hint['cell']} -> {hint['value']} | {hint['reason']}") 
    print("==================")
        