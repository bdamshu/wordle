from .server import Wordle, InteractiveWordle
from .wordle_prediction import get_recommendations, modify_dataset
from collections import Counter, defaultdict
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)


class WordleSolver:
    def __init__(self, path_to_wordlist: str):
        with open(path_to_wordlist) as f:
            self._unpruned_dictionary = [word.rstrip() for word in f]
        self.dictionary = self._unpruned_dictionary

    def solve(self, game, print_guess=False, attempt_num=1):
        if attempt_num == 1:
            self.dictionary = self._unpruned_dictionary

        self.reset_constraints()
        recommendations = get_recommendations(self.dictionary)
        if print_guess:
            print('Recommendations:', *recommendations[:3])
        if isinstance(game,  InteractiveWordle):
            word_guessed, evaluation = game.evaluate()
        if isinstance(game, Wordle):
            word_guessed = recommendations[0]
            evaluation = game.evaluate(word_guessed)
        if evaluation.upper() == 'GGGGG':
            return word_guessed, attempt_num
        self.update_constraints(word_guessed, evaluation)
        self.dictionary = modify_dataset(self.dictionary, self.absent, self.present_not_at_idx,
                                            self.present_at_idx, self.absent_at_idx)
        if self.dictionary:
            attempt_num += 1
            return self.solve(game, print_guess=print_guess, attempt_num=attempt_num)
        else:
            raise ValueError('No words left in pruned dictionary.')


    def reset_constraints(self):
        self.absent = set()
        self.absent_at_idx = defaultdict(set)
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
                if (count[ltr] == 1) and (ltr not in self.present_at_idx):
                    self.absent.add(ltr)
                else:
                    self.absent_at_idx[ltr].add(idx)
                count[ltr] -= 1
            elif result.upper() == 'G':
                self.present_at_idx[ltr].add(idx)
                count[ltr] -= 1
            elif result.upper() == 'Y':
                self.present_not_at_idx[ltr].add(idx)
                count[ltr] -= 1
