# src/hints/engine/hint_engine.py

import pygame
from hints.heuristics.naked_singles import find_naked_singles
from hints.heuristics.naked_pairs import find_naked_pairs
from hints.heuristics.hidden_singles import find_hidden_singles

class HintEngine:
    # Map hint keys for UI to their corresponding functions
    HEURISTICS = {
        pygame.K_a: ("Naked Singles", find_naked_singles),
        pygame.K_b: ("Naked Pairs", find_naked_pairs),
        pygame.K_c: ("Hidden Singles", find_hidden_singles),
    }

    # -----------------------------------
    # Run a specific heuristic by key and return its hints.
    #
    # Args:
    #    board: Board object
    #    key: str, key corresponding to a registered heuristic
    # 
    # Returns:
    #    list[dict]: List of hint dictionaries for that technique
    # -----------------------------------
    @staticmethod
    def get_hint_by_key(board, key):
        if key not in HintEngine.HEURISTICS:
            return []
        
        technique_name, func = HintEngine.HEURISTICS[key]
        try:
            hints = func(board)
            return hints
        except Exception as e:
            print(f"Error running heuristic {technique_name}: {e}")
            return []

    @staticmethod
    def get_all_hints(board):
        # Run all heuristics and return a dictionary keyed by technique name
        all_hints = {}
        for key, (technique_name, func) in HintEngine.HEURISTICS.items():
            try:
                all_hints[technique_name] = func(board)
            except Exception as e:
                print(f"Error running heuristic {technique_name}: {e}")
                all_hints[technique_name] = []
        return all_hints