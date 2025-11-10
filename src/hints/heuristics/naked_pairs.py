# src/hints/heuristics/naked_pairs.py
from hints.utils.board_utils import get_all_candidates, cell_to_ui_cell
from hints.utils.elimination_utils import find_eliminations

#"""
# Finds all naked pairs on the board (rows, columns, blocks).
#
# Args:
#    board: Board object
#
# Returns:
#    list of dicts, each containing:
#        - 'technique': 'Naked Pairs'
#        - 'cells': list of tuples (r, c) Python-indexed
#        - 'pair': set of numbers forming the naked pairs
#        - 'scope': 'row', 'column', or 'block'
#        - 'where': list of scopes ['row', 'column', 'block']
#        - 'reason': explanation string (UI-ready 1-indexed positions)
#
def find_naked_pairs(board):
    findings = []
    size = board.size
    candidates = get_all_candidates(board)
    pair_map = {}  # (frozenset(cells), frozenset(value)) → list of scopes
    technique = 'Naked Pairs'

    def record_pair(cells, pair, scope, reason):
            key = (frozenset(cells), frozenset(pair))
            if key not in pair_map:
                pair_map[key] = {
                    "technique": "Naked Pairs",
                    "cell": cell_to_ui_cell(cells),
                    "value": set(pair),
                    "where": [scope],
                    "reason": reason,
                    "eliminations":[]}
            else:
                # Add new scope if already exists
                if scope not in pair_map[key]["where"]:
                    pair_map[key]["where"].append(scope)

    # Helper to scan a house (row, col, or block)
    def scan_house(house_cells, scope_name):
        pair_cells = {}
        for r, c in house_cells:
            if len(candidates[r][c]) == 2:
                t = tuple(sorted(candidates[r][c]))
                pair_cells.setdefault(t, []).append((r, c))
        for pair_vals, cells in pair_cells.items():
            if len(cells) == 2:
                reason = f"Cells {cell_to_ui_cell(cells)} form naked pair {pair_vals} in {scope_name}."
                record_pair(cells, pair_vals, scope_name, reason)

                # --- Find eliminations for this pair ---
                confirmed_values = [(cells[0][0], cells[0][1], v) for v in pair_vals] + \
                                   [(cells[1][0], cells[1][1], v) for v in pair_vals]
                eliminations = find_eliminations(board, confirmed_values, technique)

                pair_map[(frozenset(cells), frozenset(pair_vals))]["eliminations"].extend(eliminations)

    # --- Check rows ---
    for r in range(size):
        house_cells = [(r, c) for c in range(size)]
        scan_house(house_cells, f"row {r+1}")

    # --- Check columns ---
    for c in range(size):
        house_cells = [(r, c) for r in range(size)]
        scan_house(house_cells, f"column {c+1}")

    # --- Check 3x3 blocks ---
    for block_row in range(0, size, 3):
        for block_col in range(0, size, 3):
            house_cells = [
                (r, c)
                for r in range(block_row, block_row + 3)
                for c in range(block_col, block_col + 3)
            ]
            scan_house(house_cells, f"block starting at ({block_row+1},{block_col+1})")

    return list(pair_map.values())