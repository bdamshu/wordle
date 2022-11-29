from collections import Counter

class Wordle:
    def __init__(self, word):
        assert len(word) == 5
        self.word = word
        self.chars = set(word)

    def evaluate(self, guess):
        assert len(guess) == 5
        evaluation = ['x'] * 5
        counts = Counter(self.word) # To ensure that the same letter is not used for G and Y

        # Look for greens first, so as not to reuse same letter for both green and yello
        for idx in range(5):
            guess_ltr = guess[idx]
            word_ltr = self.word[idx]

            if guess_ltr == word_ltr:
                evaluation[idx] = 'G'
                counts[word_ltr] -= 1

        # Now look for yellows
        for idx in range(5):
            guess_ltr = guess[idx]
            if evaluation[idx]!='G' and guess[idx] in self.chars and counts[guess_ltr] :
                evaluation[idx] = 'Y'
                counts[guess[idx]] -= 1

        eval_str = ''.join(evaluation)
        return eval_str


class InteractiveWordle:

    def __init__(self):
        pass

    def evaluate(self):
        word_guessed = input('Word guess: ')    # not safe to assume 1st prediction will be accepted in NYT.
        confirm = 'n'
        while confirm != 'y':
            evaluation = input('Evaluation: ')
            confirm = input('Confirm [y/n]: ')
            # Some validation
            if len(evaluation) != 5:
                confirm = 'n'

        return word_guessed, evaluation
