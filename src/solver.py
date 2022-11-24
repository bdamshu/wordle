from .server import Wordle
from .wordle_prediction import get_recommendations, modify_dataset
from collections import Counter, defaultdict
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)


class WordleSolver:
    def __init__(self, path_to_wordlist: str):
        with open(path_to_wordlist) as f:
            self.dictionary = [word.rstrip() for word in f]

    def solve(self, game: Wordle, print_guess=False):
        if len(self.dictionary) == 1:
            if print_guess:
                print(self.dictionary[0])
        else:
            self.reset_constraints()
            recommendations = get_recommendations(self.dictionary)
            if print_guess:
                print(*recommendations[:3])
            word_guessed, evaluation = game.evaluate()
            self.update_constraints(word_guessed, evaluation)
            self.dictionary = modify_dataset(self.dictionary, self.absent, self.present_not_at_idx, self.present_at_idx)
            self.solve(game, print_guess=True)


    def reset_constraints(self):
        self.absent = set()
        self.present_at_idx = defaultdict(set)
        self.present_not_at_idx = defaultdict(set)


    ##########  Useful functions ################

    def update_constraints(self, guess, evaluate):
        ''' Converts from a guess and evaluation string (e.g.xxGYx) to a set of constraints
        Constraints are saved until reset.
        '''
        count = Counter(guess)
        for idx, ltr in enumerate(guess):
            result = evaluate[idx]
            if result.lower() == 'x':
                if count[ltr] == 1:
                    self.absent.add(ltr)
                count [ltr] -= 1
            elif result.upper() == 'G':
                self.present_at_idx[ltr].add(idx)
            elif result.upper() == 'Y':
                self.present_not_at_idx[ltr].add(idx)


