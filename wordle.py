#!/usr/bin/env python
# coding: utf-8

# In[1]:


from english_words import english_words_lower_set

words_5_letters = [ word for word in english_words_lower_set
                   if (len(word) == 5) and ("'" not in word) and ('.' not in word) ]
print(f'There are {len(words_5_letters)} 5-letter english words.')


# In[2]:


# calculate probability of each letter, and
# calculate probability of each letter at position 0, 1, 2, 3, 4

from collections import Counter

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


# In[3]:


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


# In[4]:


# identify words which don't have repeating letters

def get_words_unique_letters(dataset):
    words_unique_letters = []
    for weight, word in dataset:
        if len(set(word)) == 5:
            words_unique_letters.append( (weight, word) )
        
    return words_unique_letters


# In[5]:


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
            for letter, position in present_letters_wrong_pos.items():
                if word[position] == letter:
                    match = True
                    break
                else:
                    match = False
            if match:
                continue
            if not set(word).isdisjoint(set(present_letters_wrong_pos.keys())):
                reduced_dataset.append(word)
        dataset = reduced_dataset
        
    if present_letters_correct_pos:
        reduced_dataset = []
        for word in dataset:
            for letter, position in present_letters_correct_pos.items():
                if word[position] != letter:
                    match = False
                    break
                else:
                    match = True
            if match:
                reduced_dataset.append(word)
        dataset = reduced_dataset
        
    return dataset


# In[7]:


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


# In[8]:


initial_recommendations = get_recommendations(words_5_letters)
print(f'There are {len(initial_recommendations)} recommendations.')
print(f'Best guess: {initial_recommendations[0]}')


# In[9]:


# guess1 = saute

absent_letters = ['u', 't', 'e']
present_letters_wrong_pos = {'a': 1}
present_letters_correct_pos = {'s': 0}
reduced_dataset = modify_dataset(words_5_letters, absent_letters, present_letters_wrong_pos, present_letters_correct_pos)
recommendations = get_recommendations(reduced_dataset)
print(f'There are {len(recommendations)} recommendations.')
print(f'Best guess: {recommendations[0]}')


# In[10]:


# guess2 = shark

absent_letters = ['h', 'k']
present_letters_wrong_pos = None
present_letters_correct_pos = {'s': 0, 'a': 2, 'r': 3}
reduced_dataset = modify_dataset(reduced_dataset, absent_letters, present_letters_wrong_pos, present_letters_correct_pos)
recommendations = get_recommendations(reduced_dataset)
print(f'There are {len(recommendations)} recommendations.')
print(f'Best guess: {recommendations[0]}')


# In[11]:


# guess3 = scary

absent_letters = ['c', 'y']
present_letters_wrong_pos = None
present_letters_correct_pos = {'s': 0, 'a': 2, 'r': 3}
reduced_dataset = modify_dataset(reduced_dataset, absent_letters, present_letters_wrong_pos, present_letters_correct_pos)
recommendations = get_recommendations(reduced_dataset)
print(f'There are {len(recommendations)} recommendations.')
print(f'Best guess: {recommendations[0]}')

