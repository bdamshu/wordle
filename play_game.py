from server import Wordle
from solver import WordleSolver
from scipy.stats import describe
from tqdm import tqdm


wordlist_path = '<put in wordlist path here>'
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


