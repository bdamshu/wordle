from src.server import InteractiveWordle
from src.solver import WordleSolver


game = InteractiveWordle()
wordlist_path = r'wordlists/five_letter_words_english_words.txt'
solver = WordleSolver(wordlist_path)

solver.solve(game, print_guess=True)
