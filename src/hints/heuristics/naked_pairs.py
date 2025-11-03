# src/hints/heuristics/naked_pairs.py
from hints.utils.board_utils import get_all_candidates, cell_to_ui_cell

#"""
# Finds all naked pairs on the board (rows, columns, blocks).
#
# Args:
#    board: Board object
#
# Returns:
#    list of dicts, each containing:
#        - 'technique': 'Naked Pair'
#        - 'cells': list of tuples (r, c) Python-indexed
#        - 'pair': set of numbers forming the naked pair
#        - 'scope': 'row', 'column', or 'block'
#        - 'where': list of scopes ['row', 'column', 'block']
#        - 'reason': explanation string (UI-ready 1-indexed positions)
#
def find_naked_pairs(board):
    findings = []
    size = board.size
    candidates = get_all_candidates(board)
    pair_map = {}  # (frozenset(cells), frozenset(value)) → list of scopes

    def record_pair(cells, pair, scope, reason):
            key = (frozenset(cells), frozenset(pair))
            if key not in pair_map:
                pair_map[key] = {"technique": "Naked Pair", "cell": cells, "value": set(pair), "where": [scope], "reason": reason}
            else:
                # Add new scope if already exists
                if scope not in pair_map[key]["where"]:
                    pair_map[key]["where"].append(scope)

    # Check rows for naked pairs
    for r in range(size):
        pair_cells = {}
        for c in range(size):
            if len(candidates[r][c]) == 2:
                t = tuple(sorted(candidates[r][c]))
                pair_cells.setdefault(t, []).append((r, c))
        for pair, cells in pair_cells.items():
            if len(cells) == 2:
                reason = f"Cells {cell_to_ui_cell(cells)} form naked pair {pair} in row {r+1}." # remove num elsewhere in row.
                record_pair(cell_to_ui_cell(cells), pair, "row", reason)
        
    # --- Check columns ---
    for c in range(size):
        pair_cells = {}
        for r in range(size):
            if len(candidates[r][c]) == 2:
                t = tuple(sorted(candidates[r][c]))
                pair_cells.setdefault(t, []).append((r, c))
        for pair, cells in pair_cells.items():
            if len(cells) == 2:
                reason = f"Cells {cell_to_ui_cell(cells)} form naked pair {pair} in column {c+1}." #remove these numbers elsewhere in the column.
                record_pair(cell_to_ui_cell(cells), pair, "column", reason)
    
    # --- Check blocks ---
    for block_row in range(0, size, 3):
        for block_col in range(0, size, 3):
            pair_cells = {}
            for r in range(block_row, block_row + 3):
                for c in range(block_col, block_col + 3):
                    if len(candidates[r][c]) == 2:
                        t = tuple(sorted(candidates[r][c]))
                        pair_cells.setdefault(t, []).append((r, c))
            for pair, cells in pair_cells.items():
                if len(cells) == 2:
                    reason = f"Cells {cell_to_ui_cell(cells)} form naked pair {pair} in block starting at ({block_row+1}, {block_col+1})." #remove these numbers elsewhere in the block.
                    record_pair(cell_to_ui_cell(cells), pair, "block", reason)

        # Merge all consolidated findings
        findings = list(pair_map.values())
    return findings