from collections import Counter
from pathlib import Path
import sys

root_dir = Path(__file__).resolve().parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import src.wordle_prediction as wordle_prediction

def test_get_letter_probabilities():
    dataset = ['apple', 'bison', 'morph']
    letters_total_count, letters_position_count = wordle_prediction.get_letter_probabilities(dataset)
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
    assert letters_position_count == {0: Counter({'a': 1, 'b': 1, 'm': 1}),
                                        1: Counter({'p': 1, 'i': 1, 'o': 1}),
                                        2: Counter({'p': 1, 's': 1, 'r': 1}),
                                        3: Counter({'l': 1, 'o': 1, 'p': 1}),
                                        4: Counter({'e': 1, 'n': 1, 'h': 1}),}, 'letter counts per position do not match'

def test_get_weight_per_word():
    dataset = ['apple', 'bison', 'morph']
    letters_total_count, letters_position_count = wordle_prediction.get_letter_probabilities(dataset)
    word_wieghts = wordle_prediction.get_weight_per_word(dataset, letters_total_count, letters_position_count)
    word_wieghts = [(round(weight, 6), word) for weight, word in word_wieghts]
    assert word_wieghts == [(round(9/45, 6), 'apple'), (round(8/45, 6), 'morph'), (round(6/45, 6), 'bison')]

def test_get_words_unique_letters():
    dataset = [(0, 'apple'), (0, 'bison'), (0, 'morph')]
    unique_letters_words = wordle_prediction.get_words_unique_letters(dataset)
    assert unique_letters_words == [(0, 'bison'), (0, 'morph')]

def test_modify_dataset():
    dataset = ['apple', 'amass', 'asset', 'bison', 'morph']
    absent_letters = wordle_prediction.modify_dataset(dataset, set('p'), None, None)
    assert absent_letters == ['amass', 'asset', 'bison']
    present_letters_wrong_position = wordle_prediction.modify_dataset(dataset, None, {'m': {2}}, None)
    assert present_letters_wrong_position == ['amass', 'morph']
    present_letters_correct_position = wordle_prediction.modify_dataset(dataset, None, None, {'s': {2}})
    assert present_letters_correct_position == ['asset', 'bison']