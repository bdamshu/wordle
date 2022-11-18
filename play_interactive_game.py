from src.server import InteractiveWordle
from src.solver import WordleSolver


game = InteractiveWordle()
wordlist_path = 'wordlist_path_here'
solver = WordleSolver(wordlist_path)

solver.solve(game, print_guess=True)
