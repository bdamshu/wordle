from collections import Counter
from pathlib import Path
import sys

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import src.wordle_prediction as wordle_prediction

def test_get_letter_probabilities():
    dataset = ['apple', 'bison', 'morph']
    letters_total_count = wordle_prediction.get_letter_probabilities(dataset)
    assert letters_total_count == Counter({'a': 1,
                                            'p': 3,
                                            'l': 1,
                                            'e': 1,
                                            'b': 1,
                                            'i': 1,
                                            's': 1,
                                            'o': 2,
                                            'n': 1,
                                            'm': 1,
                                            'r': 1,
                                            'h': 1}), 'overall letter counts do not match'

def test_get_weight_per_word():
    dataset = ['apple', 'bison', 'morph']
    letters_total_count = wordle_prediction.get_letter_probabilities(dataset)
    dataset +=  ['zebra']
    word_wieghts = wordle_prediction.get_weight_per_word(dataset, letters_total_count)
    assert word_wieghts == [(9, 'apple'), (6, 'morph'), (2, 'bison')]

def test_modify_dataset():
    dataset = ['apple', 'amass', 'asset', 'bison', 'morph']

    guessed_words = wordle_prediction.modify_dataset(dataset, None, None, None, ['morph'])
    assert guessed_words == ['apple', 'amass', 'asset', 'bison']

    absent_letters = wordle_prediction.modify_dataset(dataset, set('p'), None, None, None)
    assert absent_letters == ['amass', 'asset', 'bison']

    present_letters_wrong_position = wordle_prediction.modify_dataset(dataset, None, {'m': {1}}, None, None)
    assert present_letters_wrong_position == ['morph']

    present_letters_correct_position = wordle_prediction.modify_dataset(dataset, None, None, {'s': {2}}, None)
    assert present_letters_correct_position == ['asset', 'bison']