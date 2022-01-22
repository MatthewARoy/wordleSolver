# wordleSolver

A quick solver for the popular game Wordle found at https://www.powerlanguage.co.uk/wordle/

It will analyze the set of valid scrabble words and find the guess that best narrows down the remaining possibilities

After you enter the prompted guess, enter the response to the guess (the output of what is displayed in wordle)

Responses to a guess are entered as a string 5 characters long with the follow values
class LetterResult(IntEnum):
    EXCLUDED = 0
    WRONG_LOCATION = 1
    CORRECT = 2

For a guess that's green green grey yellow yellow
This maps to 22011
