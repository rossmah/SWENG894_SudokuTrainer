# SWENG894_SudokuTrainer

SudokuTrainer is a Python-based desktop application made to combine Sudoku gameplay with an interactive training experience. The system will allow users to play a variety of random Sudoku puzzles while providing hints and strategy explanations to improve their solving skills. Players will be able to generate puzzles at various difficulty levels, input custom puzzles, and use features such as pencil notes, conflict highlighting, and a guided hint system.

The project is being developed as a capstone MVP for the Penn State Software Engineering program. The application is built with Python and Pygame, and is packaged as a standalone executable for cross-platform use.

# To run (from root directory)
1. cd src
2. python3 -m main

# To run tests (from root directory)
1. PYTHONPATH=src pytest tests
OR (with coverage analysis):
2. PYTHONPATH=src python3 -m pytest --cov=src tests