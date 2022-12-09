from src.server import Wordle
from src.solver import WordleSolver
from scipy.stats import describe
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

if __name__ == '__main__':
    wordlist_path = r'wordlists/five_letter_words_english_words.txt'
    solver = WordleSolver(wordlist_path)
    all_words = solver._unpruned_dictionary

    with Pool(processes=cpu_count()) as pool:
        results = list( tqdm( pool.imap(solver.solve, [(idx, Wordle(word)) for idx, word in enumerate(all_words)]) , total=len(all_words) ) )

    wrong_guesses = []
    for idx, word_guessed, attempts in results:
        if word_guessed != all_words[idx]:
            wrong_guesses.append( (all_words[idx], word_guessed) )
    if wrong_guesses:
        print('There are wrong guesses.')
        with open('wrong_guesses.txt', 'w') as f:
            f.write('\n'.join(f'{word} guessed as {guess}' for word, guess in wrong_guesses))

    results.sort(key=lambda tup: tup[2], reverse=True)
    with open('summary.txt', 'w') as f:
        f.write('\n'.join(f'{attempts}, {word}' for _, word, attempts in results))
    print( describe([attempts for _, _, attempts in results]))