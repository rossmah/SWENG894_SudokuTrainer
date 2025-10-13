# ui/board.py
import pygame

GRID_SIZE = 9
GRID_LINE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 255)  # for selected cell
GIVEN_COLOR = (0, 0, 0)      # black for givens
USER_COLOR = (50, 50, 200)   # optional color if later we let user enter numbers
ROWCOL_HIGHLIGHT_COLOR = (220, 220, 220)  # light grey for row/col/block
CONFLICT_COLOR = (255, 100, 100)  # red tint for conflicts
MATCH_HIGHLIGHT_COLOR = (144, 238, 144)  # light green for common cells

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

        # Notes mode
        self.notes_mode = False
        self.notes = [[set() for _ in range(self.size)] for _ in range(self.size)]

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
                                c * self.cell_size,
                                r * self.cell_size,
                                self.cell_size,
                                self.cell_size
                            )
                            pygame.draw.rect(screen, MATCH_HIGHLIGHT_COLOR, match_rect)
            # Highlight all conflicts in red
            row, col = self.selected_cell
            block_row = (row // 3) * 3
            block_col = (col // 3) * 3
            for r in range(self.size):
                for c in range(self.size):
                    if r == row or c == col or (block_row <= r < block_row + 3 and block_col <= c < block_col + 3):
                        rect = pygame.Rect(
                            c * self.cell_size,
                            r * self.cell_size,
                            self.cell_size,
                            self.cell_size
                        )
                        pygame.draw.rect(screen, ROWCOL_HIGHLIGHT_COLOR, rect)
            for (r, c) in self.get_conflicts(row, col):
                rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, CONFLICT_COLOR, rect)

        # Draw grid cells
        for row in range(self.size):
            for col in range(self.size):
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                # Highlight selected cell
                if self.selected_cell == (row, col):
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect)

                # draw border
                pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)
                
                # Draw numbers: givens first, then user_board               
                num = self.user_board[row][col]
                if num != 0:
                    if self.givens[row][col] != 0:
                    # Given number - black
                        color = GIVEN_COLOR
                    elif self.locked[row][col]:
                        # Correct user entry - blue
                        color = USER_COLOR
                    else:
                        # Incorrect user entry - red
                        color = (255, 0, 0)
                    label = self.font.render(str(num), True, color)
                    label_rect = label.get_rect(center=rect.center)
                    screen.blit(label, label_rect)

                # Draw notes - only if cell is empty
                notes = self.notes[row][col]
                if notes and self.user_board[row][col] == 0:
                    for note in notes:
                        sub_row = (note - 1) // 3
                        sub_col = (note - 1) % 3
                        x = col * self.cell_size + (sub_col + 0.5) * (self.cell_size / 3)
                        y = row * self.cell_size + (sub_row + 0.5) * (self.cell_size / 3)
                        note_font = pygame.font.SysFont("arial", self.cell_size // 4)
                        note_label = note_font.render(str(note), True, (120, 120, 120))
                        note_rect = note_label.get_rect(center=(x, y))
                        screen.blit(note_label, note_rect)

        # Draw thicker lines every 3 cells (classic Sudoku style)
        for i in range(self.size + 1):
            line_width = 3 if i % 3 == 0 else 1
            # Vertical lines
            pygame.draw.line(
                screen, GRID_LINE_COLOR,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.screen_size),
                line_width
            )
            # Horizontal lines
            pygame.draw.line(
                screen, GRID_LINE_COLOR,
                (0, i * self.cell_size),
                (self.screen_size, i * self.cell_size),
                line_width
            )

    def get_cell_from_mouse(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.size and 0 <= col < self.size:
            return (row, col)
        return None

    def handle_key(self, key):
        #Convert a key press into a number entry or deletion.
        if key in range(pygame.K_1, pygame.K_9 + 1):
            number = key - pygame.K_0
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
            if number == 0:
                self.notes[row][col].clear()
            elif number in self.notes[row][col]:
                self.notes[row][col].remove(number)
            else:
                self.notes[row][col].add(number)
            return  # stop here, do not place number in user_board

        # ----- Solve mode -----
        if number == 0:
            # Clear only if not locked
            self.user_board[row][col] = 0
            return
        
        # Place number
        self.user_board[row][col] = number

        # If correct, lock it
        if self.solution and number == self.solution[row][col]:
            self.locked[row][col] = 1
    
    def toggle_notes_mode(self):
        self.notes_mode = not self.notes_mode
