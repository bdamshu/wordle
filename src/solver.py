from .server import Wordle, InteractiveWordle
from .wordle_prediction import get_recommendations
from collections import Counter, defaultdict
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)


class WordleSolver:
    def __init__(self, path_to_wordlist: str):
        with open(path_to_wordlist) as f:
            self._unpruned_dictionary = [word.rstrip() for word in f]

    def solve(self, idx_game_tup):
        word_idx, game = idx_game_tup
        guess_num = 0
        evaluation = 'xxxxx'
        self.reset_constraints()
        while evaluation.upper() != 'GGGGG':
            self.dictionary = get_recommendations(self.dictionary, self.absent, self.present_at_idx,
                                                        self.present_not_at_idx, self.guessed_words)
            if isinstance(game, Wordle):
                word_guessed = self.dictionary[0]
                evaluation = game.evaluate(word_guessed)
            elif isinstance(game, InteractiveWordle):
                print('Recommendations:', self.dictionary[:3])
                word_guessed, evaluation = game.evaluate()
            else:
                raise TypeError('Unrecognized game type.')

            guess_num += 1
            self.update_constraints(word_guessed, evaluation)
        return word_idx, word_guessed, guess_num

    def reset_constraints(self):
        self.dictionary = self._unpruned_dictionary
        self.absent = set()
        self.present_at_idx = defaultdict(set)
        self.present_not_at_idx = defaultdict(set)
        self.guessed_words = []


    ##########  Useful functions ################

    def update_constraints(self, guess, evaluate):
        ''' Converts from a guess and evaluation string (e.g.xxGYx) to a set of constraints
        Constraints are saved until reset.
        '''
        self.guessed_words.append(guess)
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
