from src.server import Wordle
from src.solver import WordleSolver
from scipy.stats import describe
from tqdm import tqdm


wordlist_path = r'wordlists/five_letter_words_english_words.txt'
solver = WordleSolver(wordlist_path)
all_words = solver.dictionary

solutions = {}
results = []
for word in tqdm(all_words):
    game = Wordle(word)

    try:
        guess, attempts = solver.solve(game)
    except ValueError:
        print(f'Can not solve {word}')

    results.append(attempts)
    if word != guess:
        print(f'Wrong solution for {word}')

print( describe(results) )


