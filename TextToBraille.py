from src import AlphaBrailleMapper, BrailleAlphaMapper

CAPITAL = chr(10272)  # ⠠
NUMBER = chr(10300)  # ⠼
UNRECOGNIZED = '?'

open_quotes = True


def extract_words(string):
    # Split up a sentence based on whitespace (" ") and new line ("\n") chars.
    words = string.split(" ")
    result = []
    for word in words:
        temp = word.split("\n")
        for item in temp:
            result.append(item)
    return result


def t2b_translate(string):
    # Convert alphabetic text to braille.
    braille = ""
    words = extract_words(string)
    for word in words:
        word = numbers_handler(word)
        word = capital_letters_handler(word)
        trimmed_word = trim(word)  # Remove punctuation (ex: change dog?" to dog)
        untrimmed_word = word
        index = untrimmed_word.find(trimmed_word)
        shavings = untrimmed_word.replace(trimmed_word, "")
        braille = build_braille_word(trimmed_word, shavings, index, braille) + " "
    return braille[:-1]  # Remove the final space that was added.


def is_braille(char):
    # Return true if a char is braille.
    if len(char) > 1:
        return False
    return char in BrailleAlphaMapper.letters or char in BrailleAlphaMapper.numbers \
           or char in BrailleAlphaMapper.punctuation or char in BrailleAlphaMapper.contractions \
           or char == CAPITAL or char == NUMBER


def find_utf_code(char):
    # Find the UTF code of a particular character. Used what an unidentified char is found.
    if len(char) != 1:
        return -1
    for i in range(0, 55000):
        if char == chr(i):
            return i


def char_to_braille(char):
    # Convert an alphabetic char to braille.
    if is_braille(char):
        return char
    elif char == "\n":
        return "\n"
    elif char == "\"":
        global open_quotes
        if open_quotes:
            open_quotes = not open_quotes
            return AlphaBrailleMapper.punctuation.get("“")
        else:
            open_quotes = not open_quotes
            return AlphaBrailleMapper.punctuation.get("”")
    elif char in AlphaBrailleMapper.letters and char.isupper():
        return CAPITAL + AlphaBrailleMapper.letters.get(char)
    elif char in AlphaBrailleMapper.letters:
        return AlphaBrailleMapper.letters.get(char)
    elif char in AlphaBrailleMapper.punctuation:
        return AlphaBrailleMapper.punctuation.get(char)
    else:
        print("Unrecognized Symbol:", char, "with UTF code:", find_utf_code(char))
        return UNRECOGNIZED


def trim(word):
    # Remove punctuation around a word. Example: cat." becomes cat
    while len(word) is not 0 and not word[0].isalnum():
        word = word[1:]
    while len(word) is not 0 and not word[-1].isalnum():
        word = word[:-1]
    return word


def numbers_handler(word):
    # Replace each group of numbers in a word to their respective braille representation.
    if word == "":
        return word
    result = word[0]
    if word[0].isdigit():
        result = NUMBER + AlphaBrailleMapper.numbers.get(word[0])
    for i in range(1, len(word)):
        if word[i].isdigit() and word[i - 1].isdigit():
            result += AlphaBrailleMapper.numbers.get(word[i])
        elif word[i].isdigit():
            result += NUMBER + AlphaBrailleMapper.numbers.get(word[i])
        else:
            result += word[i]
    return result


def capital_letters_handler(word):
    # Put the capital escape code before each capital letter.
    if word == "":
        return word
    result = ""
    for char in word:
        if char.isupper():
            result += CAPITAL + char.lower()
        else:
            result += char.lower()
    return result


def word_to_braille(word):
    # Convert an alphabetic word to braille.
    if word in AlphaBrailleMapper.contractions:
        return AlphaBrailleMapper.contractions.get(word)
    else:
        result = ""
        for char in word:
            result += char_to_braille(char)
        return result


def build_braille_word(trimmed_word, shavings, index, braille):
    # Translate a trimmed word to braille then re-attach the shavings.
    if shavings == "":
        braille += word_to_braille(trimmed_word)
    else:
        for i in range(0, len(shavings)):
            if i == index and trimmed_word is not "":
                braille += word_to_braille(trimmed_word)
            braille += word_to_braille(shavings[i])
        if index == len(shavings):  # If the shavings are all at the beginning.
            braille += word_to_braille(trimmed_word)
    return braille
