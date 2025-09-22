import random

GRID_SIZE = 9
BOX_SIZE = 3

def valid(board, row, col, num):
    # Check row & col
    if num in board[row]: return False
    if num in [board[r][col] for r in range(GRID_SIZE)]: return False
    
    # Check 3x3 box
    start_row, start_col = (row // BOX_SIZE) * BOX_SIZE, (col // BOX_SIZE) * BOX_SIZE
    for r in range(start_row, start_row + BOX_SIZE):
        for c in range(start_col, start_col + BOX_SIZE):
            if board[r][c] == num:
                return False
    return True

def solve(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                for num in range(1, GRID_SIZE+1):
                    if valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def fill_board(board):
    numbers = list(range(1, GRID_SIZE+1))
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                random.shuffle(numbers)
                for num in numbers:
                    if valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def remove_numbers(board, clues_target):
    #Remove numbers until only clues_target remain, guarentees unique solution."""
    cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(cells)

    while sum(cell != 0 for row in board for cell in row) > clues_target and cells:
        row, col = cells.pop()
        if board[row][col] == 0:
            continue

        backup = board[row][col]
        board[row][col] = 0

        # Copy for solver
        board_copy = [r[:] for r in board]
        solutions = [0]
        
        def count_solutions(b, solutions, limit=2):
            if solutions[0] >= limit:
                return
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if b[r][c] == 0:
                        for n in range(1, GRID_SIZE+1):
                            if valid(b, r, c, n):
                                b[r][c] = n
                                count_solutions(b, solutions, limit)
                                b[r][c] = 0
                        return
            solutions[0] += 1
            
        count_solutions(board_copy, solutions)

        # If not unique, undo removal
        if solutions[0] != 1:
            board[row][col] = backup
        
    return board

def generate_sudoku(difficulty="easy"):
    board = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    fill_board(board)

    difficulty_map = {
        "easy": 40,     # 40 givens
        "medium": 32,   # 32 givens
        "hard": 25,     # 25 givens
        "expert": 18,   # 18 givens
    }

    clues_target = difficulty_map.get(difficulty, 40)  # default = easy
    puzzle = remove_numbers(board, clues_target)
    return puzzle

if __name__ == "__main__":
    puzzle = generate_sudoku()
    for row in puzzle:
        print(row)
