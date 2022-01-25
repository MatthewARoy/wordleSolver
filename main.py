from knowledge import knowledge
from constants import possible_words, guessable_words, LetterResult

# Constants
vowel_multiplier = 1
debug = False
possible_words_set = set(possible_words)
guessable_words_set = set(guessable_words)


########################################################################################################################
# Building Guess Models
########################################################################################################################
def build_letter_placement_dict(word_list):
    letter_placement_dict = {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {}
    }
    letters_in_word = {}

    for word in word_list:
        for letter in set(word):
            letters_in_word[letter] = letters_in_word.get(letter, 0) + 1
        for i, letter in enumerate(word):
            letter_placement_dict[i][letter] = letter_placement_dict[i].get(letter, 0) + 1

    for k, v in letter_placement_dict.items():
        if debug: print("Letter scoring: ",
                        sorted(letter_placement_dict[k].items(), key=lambda x: x[1], reverse=True)[:5])
    if debug: print("Total letter scoring: ", sorted(letters_in_word.items(), key=lambda x: x[1], reverse=True)[:10])

    return letter_placement_dict


def score_word_guesses(word_list, letter_placement_dict):
    word_score_dict = {}
    vowels = ['a', 'e', 'i', 'o', 'u']

    for word in word_list:
        score = 0
        for i, letter in enumerate(word):
            tiebreaker = int.from_bytes(word.encode('utf-8'), 'little') / 1e14
            score += letter_placement_dict[i].get(letter, 0) * (
                vowel_multiplier if letter in vowels else 1) + tiebreaker
        # disincentivize words with duplicate letters
        word_score_dict[word] = score * len(set(word)) / len(word)

    return word_score_dict


def find_remaining_valid_words_from_guess(guess, possible_words, guessable_words):
    score = 0
    for answer in possible_words:
        known_info = knowledge()
        known_info.update_guess(guess, wordle_guess_result(guess, answer))
        filtered_words = known_info.filter_possible_words(possible_words)
        score += len(filtered_words)
    percent_reduction = 1 - score / (len(possible_words) * len(possible_words))  # would include guessable words too
    print(guess, score, percent_reduction)
    return percent_reduction


########################################################################################################################
# I/O functions
########################################################################################################################
def print_instructions():
    print("Input a string for a guess, or press enter to use first recommended guess")
    print("Response is in form of a list of LetterResult, where LetterResult is one of:", LetterResult)


# Different guessing and answer methodologies
def user_guess_function(valid_words, valid_guessable_words, *args):
    best_guesses = sorted(
        score_word_guesses(valid_guessable_words.union(valid_words),
                           build_letter_placement_dict(valid_words)).items(),
        key=lambda x: x[1], reverse=True)
    print(f"{len(valid_words)} words remaining, recommended guesses are: ", best_guesses[:5])
    return input(f"Guess (default: {best_guesses[0][0]}): ") or best_guesses[0][0]


def best_guess_function(valid_words, valid_guessable_words, *args):
    return sorted(
        score_word_guesses(valid_guessable_words.union(valid_words),
                           build_letter_placement_dict(valid_words)).items(),
        key=lambda x: x[1], reverse=True)[0][0]


def user_result_function(guess, guessable_words, *args):
    return input(f"Guess result of guess {guess}: ")


def known_word_result_function(guess, *args):
    known_word = args[0][0]
    return wordle_guess_result(guess, known_word)


def wordle_guess_result(guess, word):
    result = []
    for i, letter in enumerate(guess):
        if letter == word[i]:
            result.append(LetterResult.CORRECT)
        # need to handle case where letter is already guessed
        elif letter in word:
            result.append(LetterResult.WRONG_LOCATION)
        else:
            result.append(LetterResult.EXCLUDED)
    return result


########################################################################################################################
# Performance Testing
########################################################################################################################

# Iterate over all possible words and determine average algorithm score
def score_algorithm():
    possible_words = possible_words_set.copy()
    res = []
    for i, word in enumerate(possible_words):
        if i % 100 == 0: print(f"Currently at {i}/{len(possible_words)} testing {word}")
        res = res + [solve_word(best_guess_function, known_word_result_function, word)]

    print("Algorithm performance was ", (sum(res) / len(res)))


def find_theoretical_best_first_guess():
    # multithread didn't seem to operate faster, will look into it later
    # pool = mp.Pool(mp.cpu_count())
    # scores = [pool.apply_async(find_remaining_valid_words_from_guess, args=(word, possible_words_set, guessable_words_set)) for word in possible_words_set]
    # pool.close()
    scores_sorted = find_theoretical_best_guess(possible_words_set, guessable_words_set)
    print("Theoretical best guess is ", scores_sorted[0], scores_sorted[0][1])
    print(scores_sorted)
    return scores_sorted[0]


# Calculate all possible guesses for all possible valid answers
def find_theoretical_best_guess(subset_possible_words, subset_guessable_words):
    scores = {}
    for guess in subset_possible_words:  # + guessable_words:
        scores[guess] = find_remaining_valid_words_from_guess(guess, subset_possible_words, subset_guessable_words)
    scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("Theoretical best guess is ", scores_sorted[0], scores_sorted[0][1])
    print(scores_sorted)
    return scores_sorted


########################################################################################################################
# Solver
########################################################################################################################
# solve a word from scratch using a function that gives result for each attempt, output is number of attempts to solve
def solve_word(guess_function, result_function, *args):
    known_information = knowledge()
    known_letters = known_information.get_known_letters()
    possible_words = possible_words_set.copy()
    guessable_words = guessable_words_set.copy()
    guess_counter = 0
    print_instructions()

    while None in known_letters and len(possible_words) > 0:
        # Make a guess
        my_guess = guess_function(possible_words, guessable_words, args)
        result = result_function(my_guess, args)

        # Update information
        guess_counter += 1
        known_information.update_guess(my_guess, result)
        possible_words = known_information.filter_possible_words(possible_words)
        guessable_words = known_information.filter_possible_words(guessable_words)
    return guess_counter


if __name__ == '__main__':
    # score_algorithm()
    # find_theoretical_best_first_guess()
    # find_remaining_valid_words_from_guess("salet", possible_words_set, guessable_words_set)
    solve_word(user_guess_function, user_result_function)
    # find_theoretical_best_first_guess()
