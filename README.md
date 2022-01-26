# wordleSolver

A quick solver for the popular game Wordle found at https://www.powerlanguage.co.uk/wordle/

You can test against past wordles of previous days by using the wayback machine
Eg: https://web.archive.org/web/20220107202803/https://www.powerlanguage.co.uk/wordle/

It will analyze the set of valid scrabble words and find the guess that best narrows down the remaining possibilities

After you enter the prompted guess, enter the response to the guess (the output of what is displayed in wordle)

Responses to a guess are entered as a string 5 characters long with the follow values
class LetterResult(IntEnum):
    EXCLUDED = 0
    WRONG_LOCATION = 1
    CORRECT = 2

For a guess that's green green grey yellow yellow
This maps to 22011


# Algorithm

My first (and so far only) attempt is fairly straightforward: Out of all possible words it could be, pick the word that individually each letter is the best in slot guess. What this means:

For the set of all possible words, calculate how likely a given letter is to occur in a given location
For example, from the starting set of all possible words

Letter scoring index 0:  [('s', 366), ('c', 198), ('b', 173), ('t', 149), ('p', 142)] (truncated to 5 most common)

Letter scoring index 1:  [('a', 304), ('o', 279), ('r', 267), ('e', 242), ('i', 202)]

Letter scoring index 2:  [('a', 307), ('i', 266), ('o', 244), ('e', 177), ('u', 165)]

Letter scoring index 3:  [('e', 318), ('n', 182), ('s', 171), ('a', 163), ('l', 162)]

Letter scoring index 4:  [('e', 424), ('y', 364), ('t', 253), ('r', 212), ('l', 156)]

Total letter scoring:  [('e', 1056), ('a', 909), ('r', 837), ('o', 673), ('t', 667), ('l', 648), ('i', 647), ('s', 618), ('n', 550), ('u', 457)]


This means that the first character of all possible words (~2.3k) is most often the letter s, second most often letter c, etc

To pick out best guess, take all possible words and score them by how likely each letter in the word is to being correct, and add a penalty for repeat letters.

*What that looks like for first guess*: 2315 words remaining, recommended guesses are:  [('saine', 1542.0), ('soare', 1528.0), ('saice', 1512.0), ('slane', 1480.0), ('soily', 1437.0)]

By guessing one of these words it's testing two things:

1. Each letter in the word is likely to be the correct letter in the correct location
2. If the letter is not correct, you have successfully ruled out the maximum number of words per that letter

Where this shines: Very rapidly reduces the possibility space of potential words.
Eg: 
```
2315 words remaining

21 words remaining

6 words remaining

1 word remaining
```

Where it struggles: If it filters down to multiple words with very common structure. Eg, "tired, fired, hired, sired" where it knows "\_ired". This a algorithm only makes hardmode guesses, so it's not optimized to pick a word that's not possible (thief) that would test all possible remaining words at once.
This means on occasion it will take an extra guess when narrowing down the last few possible letters.


# Other features
I added a brute force calculator for the optimal first guess. It takes a long time to run, since it's testing for every single word how effective that word is as a first guess, by testing it against every other possible word being the answer.

WARNING: SPOILERS
<details> 
  <summary>The best first guess is:</summary>
   The best first guess is RAISE with a >97% reduction on average

   Other good guesses are [('raise', 0.9736497348030732), ('arise', 0.9724726989443436), ('irate', 0.9724495612705195), ('arose', 0.9714811376644944), ('alter', 0.9697659642952106),
</details>

The worst guesses on average only reduce possible words by ~65% ('puppy', 0.6639956336970364), ('mamma', 0.6581951681446478), ('vivid', 0.6472503020492701), ('mummy', 0.6454694475413889), ('fuzzy', 0.6303754740657465)]


