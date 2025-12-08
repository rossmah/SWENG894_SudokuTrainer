# ui/import_menu.py

import pygame
import copy
import ui.style as style
from ui.board import Board
from core import generator

class ImportMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Create a blank board for user input
        self.board = Board(
            size=9,
            screen_size=550,
            puzzle=[[0]*9 for _ in range(9)],
            solution=None,
            import_mode=True
        )

        # Button
        self.font = style.get_title_font(30)
        self.finish_button = pygame.Rect(
            self.screen_width//2 + 160,
            self.screen_height//2,
            250,
            50
        )

    # -----------------------
    # EVENT HANDLING
    # -----------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Board click
            cell = self.board.get_cell_from_mouse(event.pos)
            if cell:
                self.board.selected_cell = cell

            # Finish button click
            if self.finish_button.collidepoint(event.pos):
                success, solved_board = self._finish_import()
                if success:
                    # Return the solved board so main.py can transition to GAME state
                    print("Valid")
                    return solved_board
                else:
                    print("Invalid puzzle! Please fix conflicts.")
                    # Could add popup or message display
                    return None

        if event.type == pygame.KEYDOWN:
            # Only allow digits 1–9 and delete
            if pygame.K_1 <= event.key <= pygame.K_9 or event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                if self.board.selected_cell:
                    self.board.handle_key(event.key)

        return None
    
    # -----------------------
    # FINISH IMPORT LOGIC
    # -----------------------
    def _finish_import(self):
        """
        Validates the imported board and solves it.
        Returns: (success: bool, solved_board: list[list[int]] or None)
        """
        user_grid = self.board.user_board
        # Check for any conflicts
        for r in range(9):
            for c in range(9):
                if self.board.get_conflicts(r, c):
                    return False, None

        # Deep copy the board to solve
        solved_board = copy.deepcopy(user_grid)
        # Use generator.solve() to solve the puzzle
        if not generator.solve(solved_board):
            # No solution exists
            return False, None

        # Puzzle is valid and solved
        return True, solved_board

    # -----------------------
    # DRAW
    # -----------------------
    def draw(self, screen):
        screen.fill(style.BACKGROUND_COLOR)

        # Title
        title_font = style.get_title_font(36)
        title_surf = title_font.render("IMPORT PUZZLE", True, style.TEXT_COLOR)
        screen.blit(title_surf, (self.screen_width//2 - title_surf.get_width()//2 + 275, 10))

        # Draw board
        self.board.draw(screen)

        # Draw Finish button
        pygame.draw.rect(screen, style.BUTTON_BLUE, self.finish_button, border_radius=50)
        finish_text = self.font.render("FINISH IMPORT", True, style.TEXT_COLOR)
        screen.blit(
            finish_text,
            (self.finish_button.centerx - finish_text.get_width()//2,
             self.finish_button.centery - finish_text.get_height()//2)
        )
