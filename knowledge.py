from constants import LetterResult

# Store known information about the current wordle and and perform operations on it
class knowledge(object):
    def __init__(self, known_letters=None, excluded_letters=None, included_letters_wrong_location=None):
        if known_letters is None:
            self.known_letters = [None]*5
        if excluded_letters is None:
            self.excluded_letters = set()
        if included_letters_wrong_location is None:
            self.included_letters_wrong_location = {}

    def filter_possible_words(self, words_to_filter):
        return set([word for word in words_to_filter.copy() if knowledge.is_possible_word(self, word)])

    def is_possible_word(self, word):
        for i, letter in enumerate(word):
            if (letter in self.excluded_letters) or (
                    letter in self.included_letters_wrong_location and i in self.included_letters_wrong_location[letter]):
                return False
            if self.known_letters[i] is not None and letter != self.known_letters[i]:
                return False
        for known_letter in self.included_letters_wrong_location.keys():
            if known_letter not in word:
                return False
        return True

    def update_guess(self, guess, result):
        for i, letter in enumerate(guess):
            value = int(result[i])
            if value == LetterResult.CORRECT:
                self.known_letters[i] = letter
                # get rid of bug when letter is in word but not that location
                if letter in self.excluded_letters:
                    self.excluded_letters.remove(letter)
            elif value == LetterResult.EXCLUDED:
                if letter not in self.known_letters:
                    self.excluded_letters.add(letter)
            elif value == LetterResult.WRONG_LOCATION:
                if letter in self.included_letters_wrong_location:
                    self.included_letters_wrong_location[letter].add(i)
                else:
                    self.included_letters_wrong_location[letter] = {i}
            else:
                raise ValueError("Invalid letter result, check yo input dawg")

    def get_known_letters(self):
        return self.known_letters

    def get_excluded_letters(self):
        return self.excluded_letters

    def get_included_letters_wrong_location(self):
        return self.included_letters_wrong_location

    def print_knowledge(self):
        print("Excluded letters: " + str(self.excluded_letters))
        print("Included letters wrong location: " + str(self.included_letters_wrong_location))
        print("Known letters: " + str(self.known_letters))
