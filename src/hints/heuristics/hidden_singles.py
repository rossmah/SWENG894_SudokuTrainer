# src/hints/heuristics/hidden_singles.py
from hints.utils.board_utils import get_all_candidates, cell_to_ui_cell
from .naked_singles import find_naked_singles

#
#    Find all hidden singles in the current board state,
#    ignoring cells that already have a naked single
#
#    Returns:
#        list of dicts: Each dict has 'technique', 'cell', 'value', 'reason', 'where'
def find_hidden_singles(board):
    hints = []
    size = board.size
    candidates = get_all_candidates(board)

    # Skip naked singles
    naked_singles = find_naked_singles(board)
    naked_cells = {hint['cell'] for hint in naked_singles}

    # Keep track of cells already assigned a hidden single number
    assigned_cells = set()

    # --- Helper function to check a unit ---
    def check_unit(unit_cells, context):
        for num in range(1, 10):
            # Count how many cells in the unit have this candidate
            candidate_cells = [cell for cell in unit_cells
                   if cell not in naked_cells and num in candidates[cell[0]][cell[1]] and board.user_board[cell[0]][cell[1]] == 0]

            if len(candidate_cells) == 1:
                cell = candidate_cells[0]
                if cell not in assigned_cells:
                    assigned_cells.add(cell)
                    ui_cell = cell_to_ui_cell([cell])[0]
                    hints.append({
                        "technique": "Hidden Single",
                        "cell": cell,
                        "value": num,
                        "reason": f"Number {num} can only go in cell {ui_cell} in {context}.",
                        "where": [context]
                    })

    # --- Row check ---
    for r in range(size):
        row_cells = [(r, c) for c in range(size)]
        check_unit(row_cells, f"row {r+1}")

    # --- Column check ---
    for c in range(size):
        col_cells = [(r, c) for r in range(size)]
        check_unit(col_cells, f"column {c+1}")

    # --- Block check ---
    for br in range(0, size, 3):
        for bc in range(0, size, 3):
            block_cells = [(r, c) for r in range(br, br+3) for c in range(bc, bc+3)]
            check_unit(block_cells, f"block starting at ({br+1},{bc+1})")

    # --- Validation step ---
    validated_hints = []
    for hint in hints:
        cell_r, cell_c = hint['cell']
        num = hint['value']
        keep = True

        for unit in hint['where']:
            if unit.startswith("row"):
                r = int(unit.split()[1]) - 1
                unit_cells = [(r, c) for c in range(size)]
            elif unit.startswith("column"):
                c = int(unit.split()[1]) - 1
                unit_cells = [(r, c) for r in range(size)]
            elif unit.startswith("block"):
                br, bc = [int(x) - 1 for x in unit.split("(")[1].split(")")[0].split(",")]
                unit_cells = [(r, c) for r in range(br, br + 3) for c in range(bc, bc + 3)]
            else:
                continue

            count = sum(1 for r, c in unit_cells
                if board.user_board[r][c] == 0 and num in candidates[r][c])

            if count != 1:
                keep = False
                break

        if keep:
                validated_hints.append(hint)

    return validated_hints