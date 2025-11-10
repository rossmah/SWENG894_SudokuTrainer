from hints.utils.board_utils import get_all_candidates

def get_visible_cells(cell):
    #Return all cells visible to the given cell (same row, col, or block)
    r, c = cell
    visible = set()

    # Same row and same column
    for i in range(9):
        visible.add((r, i))
        visible.add((i, c))

    # Same block
    block_r, block_c = 3 * (r // 3), 3 * (c // 3)
    for i in range(block_r, block_r + 3):
        for j in range(block_c, block_c + 3):
            visible.add((i, j))

    # Remove the cell itself
    visible.discard((r, c))
    return visible


def get_common_visible_cells(hinted_cells):
    #Return cells that are visible to ALL hinted cells
    if not hinted_cells:
        return set()

    common = get_visible_cells(hinted_cells[0])
    for cell in hinted_cells[1:]:
        common &= get_visible_cells(cell)
    return common

def _deduplicate_eliminations(elims):
    seen = set()
    deduped = []
    for e in elims:
        key = (e["cell"], e["remove"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    return deduped


#
#Given one or more confirmed cell values, return all candidates that
#should be removed from other cells based on Sudoku rules.
#
#Args:
#    board: Board-like object (must support .size and ideally .user_board or similar)
#    confirmed_values: list of (row, col, value) tuples using 0-indexed coordinates
#
#Returns:
#    A list of dicts like:
#    [
#        {"cell": (r, c), "remove": value, "reason": "same row"},
#        {"cell": (r, c), "remove": value, "reason": "same block"},
#        ...
#    ]
#
def find_eliminations(board, confirmed_values, technique):
    eliminations = []
    candidates = get_all_candidates(board)  # 9x9 list of sets

    # --- Naked / Hidden Singles ---
    if technique in ("Naked Singles", "Hidden Singles"):
        for hr, hc, hv in confirmed_values:
            for r in range(9):
                for c in range(9):
                    if (r, c) == (hr, hc):
                        continue
                    same_row = r == hr
                    same_col = c == hc
                    same_block = (r // 3, c // 3) == (hr // 3, hc // 3)
                    if same_row or same_col or same_block:
                        if hv in candidates[r][c]:
                            relations = []
                            if same_row:
                                relations.append("same row")
                            if same_col:
                                relations.append("same column")
                            if same_block:
                                relations.append("same block")
                            reason = ", ".join(relations) + f" as ({hr+1},{hc+1})"
                            eliminations.append({
                                "cell": (r+1, c+1),
                                "remove": hv,
                                "reason": reason
                            })

    # --- Naked Pairs ---
    elif technique == "Naked Pairs":
     # For optimization: gather affected houses (rows, cols, blocks) from confirmed_values
        
        # Extract the two cells and their shared values
        cells = list({(r, c) for (r, c, _) in confirmed_values})
        pair_values = list({v for (_, _, v) in confirmed_values})

        if len(cells) != 2 or len(pair_values) != 2:
            return eliminations  # safety check

        (r1, c1), (r2, c2) = cells
        relation_bools, relation_ids = get_cell_relation((r1, c1), (r2, c2))
        rel_row, rel_col, rel_block = relation_ids

        # Use boolean flags from get_cell_relation
        same_row, same_col, same_block = relation_bools

        related_cells = set()

        # --- Only collect cells from related regions ---
    
        # Row eliminations
        if same_row:
            r = r1  # the shared row
            for c in range(9):
                if (r, c) not in [(r1, c1), (r2, c2)]:
                    related_cells.add((r, c))

        # Column eliminations
        if same_col:
            c = c1  # the shared column
            for r in range(9):
                if (r, c) not in [(r1, c1), (r2, c2)]:
                    related_cells.add((r, c))

        # Block eliminations
        if same_block:
            block_r = (r1 // 3) * 3
            block_c = (c1 // 3) * 3
            for rr in range(block_r, block_r + 3):
                for cc in range(block_c, block_c + 3):
                    if (rr, cc) not in [(r1, c1), (r2, c2)]:
                        related_cells.add((rr, cc))


        # --- Check candidate eliminations only in related cells ---
        for (r, c) in related_cells:
            for v in pair_values:
                if v in candidates[r][c]:
                    eliminations.append({
                        "cell": (r+1, c+1),
                        "remove": v,
                        "reason": f"Naked Pair in related area (row={rel_row+1}, col={rel_col+1}, block={rel_block+1})"
                    })

    else:
        raise ValueError(f"Unsupported technique: {technique}")

    return _deduplicate_eliminations(eliminations)




# Determine how two Sudoku cells are related.
#
# Args:
#    cell1, cell2: Tuples of (row, col, value), 0-indexed.
#
# Returns:
#    relation_flags: (same_row, same_col, same_block)
#        - Each is True/False
#    relation_indices: (row_index, col_index, block_index)
#        - Row/col/block index if shared, else -1
#    
def get_cell_relation(cell1, cell2):
    r1, c1 = cell1
    r2, c2 = cell2

    same_row = r1 == r2
    same_col = c1 == c2
    same_block = (r1 // 3 == r2 // 3) and (c1 // 3 == c2 // 3)

    # Return which row/col/block they share, or -1 if not
    row_idx = r1 if same_row else -1
    col_idx = c1 if same_col else -1
    block_idx = (r1 // 3) * 3 + (c1 // 3) if same_block else -1  # block 0–8

    # First return is how the cells are related
    # Second return is where the relation/s are
    return (same_row, same_col, same_block), (row_idx, col_idx, block_idx)
