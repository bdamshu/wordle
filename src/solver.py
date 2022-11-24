from .server import Wordle
import random
from collections import Counter, defaultdict
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)


class WordleSolver:
    def __init__(self, path_to_wordlist: str):
        with open(path_to_wordlist) as f:
            self.dictionary = [word.rstrip() for word in f]

    def solve(self, game: Wordle):
        ''' Put your strategy here'''
        pass


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
            if result == 'x':
                if count[ltr] == 1:
                    self.absent.add(ltr)
                count [ltr] -= 1
            elif result == 'G':
                self.present_at_idx[ltr].add(idx)
            elif result == 'Y':
                self.present_not_at_idx[ltr].add(idx)


