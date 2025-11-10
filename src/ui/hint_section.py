# src/ui/hint_section.py
import pygame
import ui.style as style
from hints.engine.hint_engine import HintEngine
from hints.utils.board_utils import get_all_candidates, pretty_print_findings


class HintSection:
    def __init__(self, board, screen_width, padding=20):
        self.board = board
        self.screen_width = screen_width
        self.padding = padding
        self.bottom_padding = 10

        # UI constants
        self.title = "HINTS"
        self.title_font = style.get_title_font(20)
        self.button_font = style.get_default_font(16)
        self.hint_font = pygame.font.SysFont("arial", 14)
        self.button_height = 36 # Heuristic Buttons
        self.button_margin = 8
        self.hint_button_spacing = 15

        # Panel geometry - position top just below the title area used by Sidebar
        sidebar_width = self.screen_width - self.board.screen_size
        hint_width = sidebar_width - 2 * self.padding
        hint_x = self.board.screen_size + (sidebar_width - hint_width) // 2
        hint_y = self.padding + 100  # leave some room for overall header
        hint_height = self.board.screen_size - hint_y - self.padding
        self.hint_rect = pygame.Rect(hint_x, hint_y, hint_width, hint_height)

        # Hint Section Scroll
        self.scroll_y = 0           # Current vertical scroll offset
        self.scroll_speed = 20      # Pixels to scroll per wheel event
        self.total_content_height = 0
        
        # Hint Section 'Show' button and highlighting
        self.hints = {}  # {heuristic_name: [list of hint dicts]}
        self.expanded_heuristic = None
        
        # Store rects of "Show" buttons for click detection
        self.show_button_rects = []

        # Open/expand heuristics
        self.open_heuristics = {}  # key: heuristic name, value: bool (open/closed)
        self._init_buttons()

    def _init_buttons(self):
        # Initialize heuristic buttons
        self.buttons = [] 
        for key, (name, _) in HintEngine.HEURISTICS.items():
            self.open_heuristics[name] = False
            self.buttons.append(name)  # store names; rects computed dynamically

    def handle_event(self, event, board):
        # Handle mouse clicks on buttons to expand/collapse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            # Check clicks on "Show" buttons
            for rect, hint in self.show_button_rects:
                if rect.collidepoint(mouse_pos):
                    cells = hint.get("cell")
                    values = hint.get("value")

                    # Normalize to lists
                    cell_list = cells if isinstance(cells, list) else [cells]
                    value_list = values if isinstance(values, (list, set, tuple)) else [values]

                    # Highlight only relevant candidates
                    board.highlight_cells([{"cell": cell_list, "value": value_list}])
                    board.highlight_eliminations(hint["eliminations"])
                    return  # Handle one click per event

            # Check heuristic button clicks (expand/collapse)
            for name, btn_rect in self._button_rects.items():
                if btn_rect.collidepoint(mouse_pos):
                    self.open_heuristics[name] = not self.open_heuristics.get(name, False)
                    return

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= int(event.y * self.scroll_speed)

            # Clamp scroll to content height
            scroll_rect = self._scroll_rect()
            max_scroll = max(0, self.total_content_height - scroll_rect.height)
            self.scroll_y = max(0, min(self.scroll_y, max_scroll))
    
    def _compute_panel_rect(self):
        # Compute the main hint panel rect
        sidebar_width = self.screen_width - self.board.screen_size
        hint_width = sidebar_width - 2 * self.padding
        hint_x = self.board.screen_size + (sidebar_width - hint_width) // 2
        hint_y = self.padding + 80  # + 80 to avoid overlapping other UI
        hint_height = self.board.screen_size - self.padding - 70
        self.hint_rect = pygame.Rect(hint_x, hint_y, hint_width, hint_height)

    def _scroll_rect(self):
        # Returns the rect of the scrollable area (below title/divider)
        title_height = self.title_font.get_height()
        divider_y = self.hint_rect.top + self.padding // 2 + title_height + 8
        return pygame.Rect(
            self.hint_rect.left,
            divider_y + 10,
            self.hint_rect.width,
            self.hint_rect.bottom - (divider_y + 12)
        )
    
    def _update_content_height(self):
        # Update total content height based on which sections are expanded
        y = 0
        for name in self.buttons:
            y += self.button_height + self.button_margin
            if self.open_heuristics.get(name, False):
                hints = HintEngine.get_all_hints(self.board).get(name, [])
                for hint in hints:
                    y += self.hint_font.get_height() + self.hint_button_spacing
                y += self.button_margin + 8 # extra padding to prevent last hint from getting cut off
        self.total_content_height = y + self.bottom_padding

    #
    # Draws a single hint like "(1,4) -> 4" with stylized visuals.
    # cell: tuple or list of tuples (e.g. (1,4) or [(2,7), (3,7)])
    # val: int or list of ints (e.g. 4 or [8,6])
    #
    def _draw_styled_hint(self, screen, x, y, cell, val):
        font = self.hint_font
        spacing = 6 # Between cell/s and arrow
        current_x = x

        # Normalize inputs
        cells = cell if isinstance(cell, (list, tuple)) and isinstance(cell[0], (list, tuple)) else [cell]
        values = val if isinstance(val, (list, tuple)) else [val]

        # Determine if this is a candidate list (yellow) or final value (green)
        is_candidate_list = any(isinstance(v, (set, list, tuple)) for v in values)

        # Choose color scheme
        circle_fill = style.HINT_CANDIDATE_YELLOW if is_candidate_list else style.HIGHLIGHT_GREEN
        #circle_border = (150, 120, 0) if is_candidate_list else (0, 100, 0)

        # Flatten the values
        flat_values = []
        for v in values:
            if isinstance(v, (set, list, tuple)):
                flat_values.extend(v)
            else:
                flat_values.append(v)

        # --- Draw each cell ---
        for c in cells:
            text_surf = font.render(str(c), True, style.TEXT_COLOR)
            rect = text_surf.get_rect(topleft=(current_x, y))
            bg_rect = rect.inflate(10, 6)
            pygame.draw.rect(screen, style.HIGHLIGHT_GREY, bg_rect, border_radius=8)
            #pygame.draw.rect(screen, (80, 80, 80), bg_rect, 1, border_radius=8)
            screen.blit(text_surf, rect)
            current_x += bg_rect.width + spacing

        # --- Draw arrow ---
        arrow = "→"
        arrow_font = style.get_default_font(16)
        arrow_surf = arrow_font.render(arrow, True, (0, 0, 0))
        screen.blit(arrow_surf, (current_x, y-2))
        current_x += arrow_surf.get_width() + spacing + 10

        # --- Draw values (each in rounded rectangle) ---
        for v in flat_values:
            text_surf = font.render(str(v), True, style.TEXT_COLOR)
            rect = text_surf.get_rect(topleft=(current_x, y))

            # Rounded rectangle padding
            width_padding = 10  # horizontal padding
            height_padding = 6  # vertical padding
            value_rect = rect.inflate(width_padding, height_padding)

            # Draw filled rectangle
            pygame.draw.rect(screen, circle_fill, value_rect, border_radius=5)

            # Blit the text
            screen.blit(text_surf, rect)
            
            # Move x position for next value
            current_x += value_rect.width + spacing

        return font.get_height() + self.hint_button_spacing  # return vertical space used

    def draw(self, screen):
        # compute geometry
        self._compute_panel_rect()
        self._update_content_height()

        # draw panel background & border
        pygame.draw.rect(screen, style.BACKGROUND_GRID, self.hint_rect)
        pygame.draw.rect(screen, style.GRID_BLACK_LINE, self.hint_rect, 2)

        # draw title centered at top of the panel
        title_surf = self.title_font.render(self.title, True, style.TEXT_COLOR)
        title_x = self.hint_rect.centerx - title_surf.get_width() // 2
        title_y = self.hint_rect.top + self.padding // 2
        screen.blit(title_surf, (title_x, title_y))

        # divider line under title
        divider_y = title_y + title_surf.get_height() + 8
        pygame.draw.line(screen, style.GRID_BLACK_LINE,
                         (self.hint_rect.left + self.padding, divider_y),
                         (self.hint_rect.right - self.padding, divider_y), 2)

         # Scrollable area
        scroll_rect = self._scroll_rect()
        screen.set_clip(scroll_rect)

        cur_y = -self.scroll_y
        left = scroll_rect.left + 10
        width = scroll_rect.width - 20

        self._button_rects = {}  # store rects for click detection
        self.show_button_rects.clear()

        for name in self.buttons:
            
            btn_rect = pygame.Rect(left, scroll_rect.top + cur_y, width, self.button_height)
            self._button_rects[name] = btn_rect

            # Draw heuristic button background & border
            pygame.draw.rect(screen, (230, 230, 230), btn_rect)
            pygame.draw.rect(screen, (0, 0, 0), btn_rect, 1)

            # Draw button label
            label_surf = self.button_font.render(name, True, (0, 0, 0))
            screen.blit(label_surf, (btn_rect.x + 10, btn_rect.y + (self.button_height - label_surf.get_height()) // 2))

            cur_y += self.button_height + 8  # small gap before hints
            
            # Draw hints if expanded
            if self.open_heuristics.get(name, False):
                # get hints for this heuristic
                all_hints = HintEngine.get_all_hints(self.board)
                hints = all_hints.get(name, [])
                
                for hint in hints:
                    cell = hint['cell']
                    val = hint['value']
                    used_height = self._draw_styled_hint(
                        screen,
                        btn_rect.x + 10,
                        scroll_rect.top + cur_y,
                        cell,
                        val
                    )
                    cur_y += used_height + 2

                    # Draw "Show" button
                    show_text = self.button_font.render("Show", True, style.TEXT_COLOR)
                    show_rect = pygame.Rect(
                        btn_rect.right - show_text.get_width() - 14,
                        scroll_rect.top + cur_y - used_height,
                        show_text.get_width() + 10,
                        22
                    )
                    pygame.draw.rect(screen, (200, 200, 200), show_rect)
                    pygame.draw.rect(screen, (0, 0, 0), show_rect, 1)
                    screen.blit(show_text, (show_rect.x + 5, show_rect.y + 3))
                    self.show_button_rects.append((show_rect, hint))

         # Draw scrollbar
        if self.total_content_height > scroll_rect.height:
            scrollbar_height = max(20, scroll_rect.height * scroll_rect.height // self.total_content_height)
            scrollbar_y = scroll_rect.top + (self.scroll_y / self.total_content_height) * scroll_rect.height
            pygame.draw.rect(screen, (180, 180, 180),
                             (scroll_rect.right - 8, scrollbar_y, 6, scrollbar_height))
        # Reset clipping
        screen.set_clip(None)

# ---
# Handles key events for hint heuristics.
# Args:
#        event: Pygame event
#        board: Board instance
# ---
def handle_hint_key(event, board):
    if event.type != pygame.KEYDOWN or board is None:
        return
    
    # Fill all candidates when 'f' is pressed - For testing purposes
    if event.key == pygame.K_f:
        candidates = get_all_candidates(board)
        for r in range(board.size):
            for c in range(board.size):
                if board.user_board[r][c] == 0:  # empty cell
                    board.notes[r][c] = set(candidates[r][c])
        return

    # Print hints to command line. For easy testing purposes
    # a - Naked Singles
    # b - Naked Pairs
    # c - Hidden SIngles
    if event.key in HintEngine.HEURISTICS:
        hints = HintEngine.get_hint_by_key(board, event.key)
        pretty_print_findings(hints)
