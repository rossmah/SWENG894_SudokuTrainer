# ui/style.py
import pygame
import os

pygame.font.init()

# Dynamically resolve font paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "../../assets/fonts")

# ---------- COLORS ----------
BACKGROUND_COLOR = (211, 211, 205)  # #D3D3CD
BACKGROUND_GRID = (236, 236, 236)   # ECECEC

TEXT_COLOR = (0, 0, 0)
BUTTON_BLUE = (105, 170, 231)

HIGHLIGHT_GREY = (205, 205, 205)   #CDCDCD
HIGHLIGHT_BLUE = (200, 222, 255) 
HIGHLIGHT_RED = (255, 201, 201) 
HIGHLIGHT_GREEN = (193, 226, 188)

HIGHLIGHT_WRONG_ENTRY = (255, 161, 161)
OUTLINE_WRONG_ENTRY = (228, 139, 139) # E48B8B

GRID_BLACK_LINE = (0, 0, 0)
GRID_GREY_LINE = (189, 189, 189)
GRID_OFFSET_X = 10
GRID_OFFSET_Y  = 10

GIVEN_COLOR = (0, 0, 0)      # black for givens
USER_COLOR = (50, 50, 200) 
WRONG_COLOR = (255, 0, 0)

# NumberPad colors
NUMBERPAD_BUTTON_COLOR = (230, 230, 230)
NUMBERPAD_BORDER_COLOR = (0, 0, 0)
NUMBERPAD_HOVER_COLOR = (200, 200, 200)

# Hint Section
HINT_CANDIDATE_YELLOW = (245,224,66)






'''
SELECTED_FILL_COLOR = (200, 200, 255)  # existing light blue
SELECTED_OUTLINE_COLOR = (0, 100, 255)  # strong blue outline
CONFLICT_FILL_COLOR = (255, 200, 200)  # optional, for conflicts
CONFLICT_OUTLINE_COLOR = (255, 0, 0)  # red outline
MATCH_HIGHLIGHT_COLOR = (150, 255, 150)  # for matching numbers
'''

# ---------- FONTS ----------
try:
    FONT_TITLE = pygame.font.Font(os.path.join(FONT_DIR, "MadimiOne-Regular.ttf"), 48)
    FONT_MENU = pygame.font.Font(os.path.join(FONT_DIR, "Monofett-Regular.ttf"), 54)
    FONT_TIMER = pygame.font.Font(os.path.join(FONT_DIR, "MadimiOne-Regular.ttf"), 22)
    FONT_MODE = pygame.font.Font(os.path.join(FONT_DIR, "MadimiOne-Regular.ttf"), 22)
    FONT_REGULAR = pygame.font.SysFont("arial", 24)
    
    #FONT_TITLE = pygame.font.Font("assets/fonts/MadimiOne-Regular.ttf", 48)
    #FONT_MENU = pygame.font.Font("assets/fonts/Monofett-Regular.ttf", 42)
    #FONT_TIMER = pygame.font.Font("assets/fonts/MadimiOne-Regular.ttf", 30)
    #FONT_MODE = pygame.font.Font("assets/fonts/MadimiOne-Regular.ttf", 22)
    #FONT_REGULAR = pygame.font.SysFont("arial", 24)
except Exception as e:
    print("Error loading custom fonts:", e)
    FONT_TITLE = pygame.font.SysFont("arial", 48)
    FONT_MENU = pygame.font.SysFont("arial", 36)
    FONT_TIMER = pygame.font.SysFont("arial", 30)
    FONT_MODE = pygame.font.SysFont("arial", 22)
    FONT_REGULAR = pygame.font.SysFont("arial", 24)

def load_font(filename, size):
    path = os.path.join(FONT_DIR, filename)
    return pygame.font.Font(path, size)

# Font getters
def get_title_font(size=64):
    return load_font("MadimiOne-Regular.ttf", size)

def get_menu_font(size=48):
    return load_font("Monofett-Regular.ttf", size)

def get_default_font(size=32):
    return pygame.font.SysFont("arial", size)