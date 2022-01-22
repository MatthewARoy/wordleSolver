from english_words import english_words_lower_set
from scrabble_words import scrabble_words
from enum import IntEnum

# CONSTANTS
with open("Collins Scrabble Words (2019).txt") as f:
    scrabble_file_words = f.read().split()
five_letter_words = [word for word in scrabble_file_words if len(word) == 5]
class LetterResult(IntEnum):
    EXCLUDED = 0
    WRONG_LOCATION = 1
    CORRECT = 2

def build_letter_placement_dict(word_list):
    letter_placement_dict = {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {}
    }
    for word in word_list:
        for i, letter in enumerate(word):
            letter_placement_dict[i][letter] = letter_placement_dict[i].get(letter, 0) + 1

    for k,v in letter_placement_dict.items():
        print("Letter scoring: ", sorted(letter_placement_dict[k].items(), key=lambda x: x[1], reverse=True)[:5])

    return letter_placement_dict

def score_word_guesses(word_list, letter_placement_dict):
    word_score_dict = {}
    vowels = ['A', 'E', 'I', 'O', 'U']
    vowel_bonus = 1.2

    

    for word in word_list:
        score = 0
        for i, letter in enumerate(word):
            letter_score = letter_placement_dict[i][letter]
            # incentivize vowels
            if vowels.__contains__(letter):
                letter_score = letter_score * vowel_bonus
            score += letter_score
        # disincentivize words with duplicate letters
        word_score_dict[word] = score * len(set(word)) / len(word)

    print("Best guesses: ", sorted(word_score_dict.items(), key=lambda x: x[1], reverse=True)[:5])
    return word_score_dict

def update_known_information(word, result, known_word, excluded_letters, included_letters_wrong_location):
    for i,letter in enumerate(word):
        value = int(result[i])
        if value == LetterResult.CORRECT:
            known_word[i] = letter
            # get rid of bug when letter is in word but not that location
            if letter in excluded_letters:
                excluded_letters.remove(letter)
        elif value == LetterResult.EXCLUDED:
            if letter not in known_word:
                excluded_letters.add(letter)
        elif value == LetterResult.WRONG_LOCATION:
            if letter in included_letters_wrong_location:
                included_letters_wrong_location[letter].add(i)
            else:
                included_letters_wrong_location[letter] = {i}
        else:
            raise ValueError("Invalid letter result, check yo input dawg")

    return known_word, excluded_letters, included_letters_wrong_location

def is_possible_word(word, known_word, excluded_letters, included_letters_wrong_location):
    for i, letter in enumerate(word):
        if (letter in excluded_letters) or (letter in included_letters_wrong_location and i in included_letters_wrong_location[letter]):
            return False
        if known_word[i] is not None and letter != known_word[i]:
            return False
    for known_letter in included_letters_wrong_location.keys():
        if not word.__contains__(known_letter):
            return False
    return True

def filter_words(word_list, excluded_letters, included_letters_wrong_location, known_word):
    return [word for word in word_list.copy() if is_possible_word(word, known_word, excluded_letters, included_letters_wrong_location)]

def find_word():
    debug = True
    my_guess = [None]*5
    possible_words = five_letter_words.copy()
    guess_counter = 0
    excluded_letters = set()
    # map of included letters to their not possible locations
    included_letters_wrong_location = {}
    while my_guess.__contains__(None) and guess_counter < 6 and len(possible_words) > 0:
        possible_words = filter_words(possible_words, excluded_letters, included_letters_wrong_location, my_guess)
        if (debug):
            print("Guess: ", my_guess)
            print("Excluded Letters: ", excluded_letters)
            print("Included Letters Wrong Location: ", included_letters_wrong_location)
            print("Total Possible Words: ", len(possible_words))
        guess_counter += 1
        if len(possible_words) == 0:
            print("Something went wrong! No possible words left!")
            return
        best_guesses = sorted(score_word_guesses(possible_words, build_letter_placement_dict(possible_words)).items(), key=lambda x: x[1], reverse=True)
        best_guess = best_guesses[0][0]
        result = "0"
        current_guess = 0
        while len(result) != 5:
            best_guess = best_guesses[current_guess][0]
            current_guess += 1
            print("My best guess is: ", best_guess)
            result = input("Guess result: ")
        my_guess, excluded_letters, included_letters_wrong_location = update_known_information(best_guess, result, my_guess, excluded_letters, included_letters_wrong_location)

    print(my_guess)



def testing_framework():
    actualWord = input("Enter a word: ")
    # test how much a guess reduced the number of possible words

if __name__ == '__main__':
    find_word()