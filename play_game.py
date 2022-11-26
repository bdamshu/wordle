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

    results.append((attempts, word))
    if word != guess:
        print(f'Wrong solution for {word}')

print( describe( [attempts for attempts, _ in results] ) )
results.sort(key=lambda tup: tup[0], reverse=True)
with open('summary.txt', 'w') as f:
    f.write('\n'.join(f'{tup[0]}, {tup[1]}' for tup in results))


