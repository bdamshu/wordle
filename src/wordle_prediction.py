#!/usr/bin/env python
# coding: utf-8

from collections import Counter


# calculate probability of each letter, and
# calculate probability of each letter at position 0, 1, 2, 3, 4
def get_letter_probabilities(dataset):
    letters_overall_count = Counter()
    letters_position_count = {}
    for word in dataset:
        for idx, letter in enumerate(word):
            letters_overall_count.update(letter)
            if idx in letters_position_count:
                letters_position_count[idx].update(letter)
            else:
                letters_position_count[idx] = Counter(letter)
                
    return letters_overall_count, letters_position_count


# calculate weight of each word: probability of letter at position 'i' * probability of letter
def get_weight_per_word(dataset, letters_overall_count, letters_position_count):
    word_weights = []
    for word in dataset:
        weight = 0
        for idx, letter in enumerate(word):
            weight += (letters_position_count[idx][letter]/sum(letters_position_count[idx].values())) * (letters_overall_count[letter]/sum(letters_overall_count.values()))
        word_weights.append( (weight, word) )
    word_weights.sort(key = lambda tup: tup[0], reverse=True)
    
    return word_weights


# identify words which don't have repeating letters
def get_words_unique_letters(dataset):
    words_unique_letters = []
    for weight, word in dataset:
        if len(set(word)) == 5:
            words_unique_letters.append( (weight, word) )
        
    return words_unique_letters


# letter is absent : remove words from dataset that contain the letter
# letter is present, correct position: remove words from dataset with letter not in position
# letter is present, wrong position: remove words from dataset without the letter, and letter in position of guess
def modify_dataset(dataset, absent_letters, present_letters_wrong_pos, present_letters_correct_pos):    
    if absent_letters:
        reduced_dataset = []
        for word in dataset:
            if set(word).isdisjoint(set(absent_letters)):
                reduced_dataset.append(word)
        dataset = reduced_dataset
    
    if present_letters_wrong_pos:
        reduced_dataset = []
        for word in dataset:
            for letter, idxs in present_letters_wrong_pos.items():
                for position in idxs:
                    if word[position] == letter:
                        match = True
                        break
                    else:
                        match = False
                if match:
                    break
            if match:
                continue
            if not set(word).isdisjoint(set(present_letters_wrong_pos.keys())):
                reduced_dataset.append(word)
        dataset = reduced_dataset
        
    if present_letters_correct_pos:
        reduced_dataset = []
        for word in dataset:
            for letter, idxs in present_letters_correct_pos.items():
                for position in idxs:
                    if word[position] != letter:
                        match = False
                        break
                    else:
                        match = True
                if not match:
                    break
            if match:
                reduced_dataset.append(word)
        dataset = reduced_dataset
        
    return dataset


def get_recommendations(dataset):
    if len(dataset) == 1:
        return dataset
    else:
        letters_overall_count, position_letters_count = get_letter_probabilities(dataset)
        weights_per_word = get_weight_per_word(dataset, letters_overall_count, position_letters_count)
        words_unique_letters = get_words_unique_letters(weights_per_word)
        if not words_unique_letters:
            print(f'No more words with non-repeating letters')
            return weights_per_word
        
        return words_unique_letters
