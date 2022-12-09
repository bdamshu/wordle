#!/usr/bin/env python
# coding: utf-8

from collections import Counter


# calculate probability of each letter
def get_letter_probabilities(dataset):
    letters_overall_count = Counter()
    for word in dataset:
        for letter in word:
            letters_overall_count.update(letter)

    return letters_overall_count


# calculate weight of each word: product across all letters in word the probability of letter
def get_weight_per_word(dataset, letters_overall_count):
    word_weights = []
    for word in dataset:
        weight = 1
        for letter in word:
            weight = weight * letters_overall_count[letter]
        if weight:
            word_weights.append( (weight, word) )
    word_weights.sort(key = lambda tup: tup[0], reverse=True)

    return word_weights


# remove already guessed words
# letter is absent : remove words from dataset that contain the letter
# letter is present, correct position: remove words from dataset with letter not in position
# letter is present, wrong position: remove words from dataset without the letter, and letter in position of guess
def modify_dataset(dataset, absent_letters, present_letters_wrong_pos, present_letters_correct_pos, guessed_words):
    reduced_dataset = []
    for word in dataset:
        valid = True

        if valid and guessed_words:
            if word in guessed_words:
                valid = False

        if valid and absent_letters:
            if not set(word).isdisjoint(absent_letters):
                valid = False

        if valid and present_letters_wrong_pos:
            if set(present_letters_wrong_pos.keys()).issubset(set(word)):
                for letter, idxs in present_letters_wrong_pos.items():
                    for position in idxs:
                        if word[position] == letter:
                            valid = False
                            break
                    if not valid:
                        break
            else:
                valid = False

        if valid and present_letters_correct_pos:
            for letter, idxs in present_letters_correct_pos.items():
                for position in idxs:
                    if word[position] != letter:
                        valid = False
                        break
                if not valid:
                    break

        if valid:
            reduced_dataset.append(word)

    return reduced_dataset

def order_words(dataset_weights, letters_present, letters_guessed):
    common_letters_dataset_weights = []
    for weight, word in dataset_weights:
        unique_letters_in_word = len(set(word))
        common_present_letters = len(set(word).intersection(letters_present))
        common_guessed_letters = len(set(word).intersection(letters_guessed))
        common_letters_dataset_weights.append( (unique_letters_in_word, common_present_letters, common_guessed_letters, weight, word) )
    common_letters_dataset_weights.sort(key=lambda tup: [tup[0], -tup[1], -tup[2], tup[3]], reverse=True)
    return common_letters_dataset_weights

def get_recommendations(dataset, absent_letters, present_at_idx_letters, present_not_at_idx_letters, guessed_words):
    present_letters = set(list(present_at_idx_letters.keys()) + list(present_not_at_idx_letters.keys()))
    letters_guessed = set()
    for word in guessed_words:
        letters_guessed.update([l for l in word])

    dataset_for_probabilities = modify_dataset(dataset, absent_letters, present_not_at_idx_letters, present_at_idx_letters, guessed_words)
    if (len(present_letters) == 5) or (len(dataset_for_probabilities) == 1):
        recommendations = dataset_for_probabilities
    else:
        letters_counts = get_letter_probabilities(dataset_for_probabilities)
        word_weights = get_weight_per_word(dataset, letters_counts)
        recommendations = order_words(word_weights, present_letters, letters_guessed)
        recommendations = [word for _, _, _, _, word in recommendations if word not in guessed_words]

    return recommendations
