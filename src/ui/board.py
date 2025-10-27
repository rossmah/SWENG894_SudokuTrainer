# ui/board.py
import pygame
import ui.style as style

GRID_SIZE = 9

class Board:
    def __init__(self, size=9, screen_size=600, puzzle=None, solution=None):
        self.size = size
        self.screen_size = screen_size
        self.cell_size = screen_size // size
        self.font = pygame.font.SysFont("arial", self.cell_size // 2)

        self.grid = puzzle if puzzle else [[0]*size for _ in range(size)]
        self.solution = solution  
        
        # Track user edits separately without harm of overwriting givens
        # - Starts as copy of puzzle (self.grid), will update as user enters numbers
        self.user_board = [row[:] for row in self.grid]  

        # Keep track of which cells are givens (non-editable)
        self.givens = [[1 if val != 0 else 0 for val in row] for row in self.grid]
        self.locked = [[0 for _ in range(size)] for _ in range(size)]

        # track selected cell (row, col)
        self.selected_cell = None
        self.selected_cell_type = None     

        # Notes mode
        self.notes_mode = False
        self.notes = [[set() for _ in range(self.size)] for _ in range(self.size)]

        # Count of how many of each number user has correctly entered
        self.number_counts = {i: 0 for i in range(1, 10)}

    def get_conflicts(self, row, col):
        # Return list of (r, c) positions that conflict with selected cell
        conflicts = []
        num = self.user_board[row][col]
        if num == 0:
            return conflicts

        # same row or column
        for i in range(self.size):
            if i != col and self.user_board[row][i] == num:
                conflicts.append((row, i))
            if i != row and self.user_board[i][col] == num:
                conflicts.append((i, col))

        # same 3x3 block
        block_row = (row // 3) * 3
        block_col = (col // 3) * 3
        for r in range(block_row, block_row + 3):
            for c in range(block_col, block_col + 3):
                if (r, c) != (row, col) and self.user_board[r][c] == num:
                    conflicts.append((r, c))
        return conflicts
       
    def draw(self, screen):
        # Draw grid background color
        grid_size = self.cell_size * 9
        grid_rect = pygame.Rect(style.GRID_OFFSET_X, style.GRID_OFFSET_Y, grid_size, grid_size)
        pygame.draw.rect(screen, style.BACKGROUND_GRID, grid_rect)

        # Draw grey highlight for row, column, and block
        if self.selected_cell:
             # Highlight all matching numbers in green
            sel_row, sel_col = self.selected_cell
            selected_value = self.user_board[sel_row][sel_col]
            if selected_value != 0:
                for r in range(self.size):
                    for c in range(self.size):
                        if (r, c) != (sel_row, sel_col) and self.user_board[r][c] == selected_value:
                            match_rect = pygame.Rect(
                                style.GRID_OFFSET_X + c * self.cell_size,
                                style.GRID_OFFSET_Y + r * self.cell_size,
                                self.cell_size,
                                self.cell_size
                            )
                            pygame.draw.rect(screen, style.HIGHLIGHT_GREEN, match_rect)
            # Highlight all conflicts in red
            row, col = self.selected_cell
            block_row = (row // 3) * 3
            block_col = (col // 3) * 3
            for r in range(self.size):
                for c in range(self.size):
                    if r == row or c == col or (block_row <= r < block_row + 3 and block_col <= c < block_col + 3):
                        rect = pygame.Rect(
                            style.GRID_OFFSET_X + c * self.cell_size,
                            style.GRID_OFFSET_Y + r * self.cell_size,
                            self.cell_size,
                            self.cell_size
                        )
                        pygame.draw.rect(screen, style.HIGHLIGHT_GREY, rect)
            for (r, c) in self.get_conflicts(row, col):
                rect = pygame.Rect(
                    style.GRID_OFFSET_X + c * self.cell_size,
                    style.GRID_OFFSET_Y + r * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, style.HIGHLIGHT_RED, rect)

        # Draw grid cells
        for row in range(self.size):
            for col in range(self.size):
                rect = pygame.Rect(
                    style.GRID_OFFSET_X + col * self.cell_size,
                    style.GRID_OFFSET_Y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                # Highlight selected cell
                if self.selected_cell == (row, col):
                    if self.givens[row][col]:
                        # Givens - Highlight selected cell in blue
                        pygame.draw.rect(screen, style.HIGHLIGHT_BLUE, rect)
                    elif self.locked[row][col]: 
                        # Correct entry - Highlight selected cell in blue
                        pygame.draw.rect(screen, style.HIGHLIGHT_BLUE, rect)
                    elif self.user_board[row][col] != 0 and self.solution:
                        # Wrong entry - Highlight selected cell in red
                        pygame.draw.rect(screen, style.HIGHLIGHT_WRONG_ENTRY, rect)
                        self.selected_cell_type="WRONG"
                    else:  # Default - Highlight selected cell in blue
                        pygame.draw.rect(screen, style.HIGHLIGHT_BLUE, rect)

                # Draw numbers: givens first, then user_board               
                num = self.user_board[row][col]
                is_wrong = self.solution and num != 0 and num != self.solution[row][col] and not self.givens[row][col]
                if num != 0:
                    if self.givens[row][col] != 0:
                    # Given number - black
                        color = style.GIVEN_COLOR
                    elif self.locked[row][col]:
                        # Correct user entry - blue
                        color = style.USER_COLOR
                    else:
                        # Incorrect user entry - red
                        color = style.WRONG_COLOR
                    label = self.font.render(str(num), True, color)
                    label_rect = label.get_rect(center=rect.center)
                    screen.blit(label, label_rect)

                # Draw notes - only if cell is empty
                notes = self.notes[row][col]
                if notes and self.user_board[row][col] == 0:
                    for note in notes:
                        sub_row = (note - 1) // 3
                        sub_col = (note - 1) % 3
                        x = style.GRID_OFFSET_X + col * self.cell_size + (sub_col + 0.5) * (self.cell_size / 3)
                        y = style.GRID_OFFSET_Y + row * self.cell_size + (sub_row + 0.5) * (self.cell_size / 3)
                        note_font = pygame.font.SysFont("arial", self.cell_size // 4)
                        note_label = note_font.render(str(note), True, (120, 120, 120))
                        note_rect = note_label.get_rect(center=(x, y))
                        screen.blit(note_label, note_rect)

        # Draw thicker lines every 3 cells (classic Sudoku style)
        for i in range(self.size + 1):
            if  i % 3 == 0:
                line_width = 3
            else:
                line_width = 1
            # Vertical lines
            pygame.draw.line(
                screen, style.GRID_BLACK_LINE,
                (style.GRID_OFFSET_X + i * self.cell_size, style.GRID_OFFSET_Y),
                (style.GRID_OFFSET_X + i * self.cell_size, style.GRID_OFFSET_Y + self.screen_size),
                line_width
            )
            # Horizontal lines
            pygame.draw.line(
                screen, style.GRID_BLACK_LINE,
                (style.GRID_OFFSET_X, style.GRID_OFFSET_Y + i * self.cell_size),
                (style.GRID_OFFSET_X + self.screen_size, style.GRID_OFFSET_Y + i * self.cell_size),
                line_width
            )

    def get_cell_from_mouse(self, pos):
        x, y = pos
        col = (x - style.GRID_OFFSET_X) // self.cell_size
        row = (y - style.GRID_OFFSET_Y) // self.cell_size
        if 0 <= row < self.size and 0 <= col < self.size:
            return (row, col)
        return None

    def handle_key(self, key):
        #Convert a key press into a number entry or deletion.
        if key in range(pygame.K_1, pygame.K_9 + 1):
            number = key - pygame.K_0
            # If all of number x is on the board, don't let user enter more
            if self.number_counts.get(number, 0) >= 9:
                return
            self.handle_number_entry(number)
        elif key in (pygame.K_BACKSPACE, pygame.K_DELETE):
            self.handle_number_entry(0) 
        else:
            return
            

    def handle_number_entry(self, number):
        #Handle number input (1–9) for non-given cells, and delete/backspace to clear
        if self.selected_cell is None:
            return
        row, col = self.selected_cell

        # Ignore givens AND locked cells
        if self.givens[row][col] == 1 or self.locked[row][col] == 1:
            return
        
        # ----- Notes mode -----
        if self.notes_mode:
            # Only allow notes in empty cells
            if self.user_board[row][col] != 0:
                return
            
            if self.number_counts[number] >= 9:
                return
            elif number in self.notes[row][col]:
                self.notes[row][col].remove(number)
            else:
                self.notes[row][col].add(number)
            return  # stop here, do not place number in user_board

        # ----- Solve mode -----
        # Place number
        self.user_board[row][col] = number

        # If correct, lock it
        if self.solution and number == self.solution[row][col]:
            self.locked[row][col] = 1
            
            # Update number counts after correct entry
            self.update_number_counts()
    
    def toggle_notes_mode(self):
        self.notes_mode = not self.notes_mode

    def update_number_counts(self):
        # Recalculate how many times each number (1–9) appears on the board
        self.number_counts = {i: 0 for i in range(1, 10)}
        for row in self.user_board:
            for num in row:
                if num in self.number_counts:
                    self.number_counts[num] += 1
