#!/usr/bin/python3
# -*-coding:utf8 -*


import re                                                   # regular expression
from Utils.FileUtils import *
import os


strings_maps_directory = os.path.dirname(os.path.abspath(__file__)) + '/StringsMaps/'
letters_maps_directory = strings_maps_directory + 'LettersMaps/'


def print_single_letters(string):
    """print single letters, ignoring A-a-I.

    :param string: the string to check.
    :return:
    """
    if re.match(r"\b[b-zB-HJ-Z]\b", string):
        print(string)

    return


def remove_space_from_word(string, word, check_uppercase, check_plural):
    """remove space from word
    "test" with every option will be checked by the regex "\b([Tt])est(?=s?\b)"

    :param string: string, input sentence to fix
    :param word: string, the word to fix.
    :param check_uppercase: boolean, check uppercase on the first letter
    :param check_plural: boolean, check even with an "s" at the end
    :return:
    """
    if check_uppercase:
        regex = r"\b([" + word[:1].upper() + word[:1] + "])" + word[1:]
    else:
        regex = r"\b(" + word[:1] + ")" + word[1:]

    if check_plural:
        regex += r"(?=s?\b)"
    else:
        regex += r"\b"

    return re.sub(r"" + regex, r"\1" + word[1:].replace(" ", ""), string)


def is_text_line(text):
    """True if not empty, not a sub number, and not a time code

    :param text: string, the string to test.
    :return: boolean
    """
    regexs = []
    regexs.append('^$')
    regexs.append('^\d{1,4}$')
    regexs.append('^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$')

    for regex in regexs:
        if re.match(regex, text):
            return False

    return True


def fix_triple_dots(string):
    """. . . => ...
    Add a space after the three dots, if there isn't, and if isn't before a linebreak

    :param string: the string to fix.
    :return: string
    """
    res = string.replace(". . .", "...")
    res = res.replace(".. .", "...")
    res = res.replace(". ..", "...")

    res = re.sub(r"\.\.\.(?!\n| )", "... ", res)
    return res


def fix_quotes(string):
    """ '' => ", and fix spaces.
    Add a space after the three dots, if there isn't, and if isn't before a linebreak

    :param string: the string to fix.
    :return: string
    """
    res = string

    res = res.replace("' '", "\"")
    res = res.replace("''", "\"")

    if re.search("\s'", res):
        for word in get_csv_words(strings_maps_directory + 'quote_word_trusted.csv'):
            res = re.sub(r"\s'" + word + r"\b", "'" + word, res)

    if re.search("'\s", res):
        print("Unknown '_ : " + res.replace("\n", ""))
    if re.search("\s'", res):
        print("Unknown _' : " + res.replace("\n", ""))

    return res


def fix_question_marks(string):
    """ *? => *_?
    Add a space after the three dots, if there isn't, and if isn't before a linebreak

    :param string: the string to fix.
    :return: string
    """
    res = string

    if "?" in string:
        res = re.sub(r"(\w)(\?)", r"\1 \2", res)

    return res


def fix_exclamation_marks(string):
    """ *! => *_!

    :param string: the string to fix.
    :return: string
    """
    res = string

    if "!" in string:
        res = re.sub(r"(\w)(!)", r"\1 \2", res)

    return res


def fix_dialog_hyphen(string):
    """Add a space after the hyphen at the beginning of a line.

    Will fix :
       *  -text       :   - text
       *  -"text      :   - "text
       *  <i>-text    :   <i>- text
       *  -<i>text    :   - <i>text
       *  "-text      :   "- text
       *  "-... text  :   "- ... text

    :param string: the string to fix.
    :return: string
    """
    res = string

    if string.startswith("\"-"):
        if not string.startswith("\"- "):
            res = re.sub(r"^\"-(\w)", r"\"- \1", res)

    elif string.startswith("-\""):
        if not string.startswith("-\" "):
            res = re.sub(r"^-\"(\w)", r"- \"\1", res)

    elif string.startswith("-<i>"):
        if not string.startswith("-<i> "):
            res = re.sub(r"^-<i>(\w)", r"- <i>\1", res)

    elif string.startswith("<i>-"):
        if not string.startswith("<i>- "):
            res = re.sub(r"^<i>-(\w)", r"<i>- \1", res)

    elif string.startswith("-..."):
        res = re.sub(r"^-\.\.\.", "- ...", res)

    elif string.startswith("-"):
        if not string.startswith("- "):
            res = re.sub(r"^-(\w)", r"- \1", res)

    return res


def fix_letter_followed_by_space(string, letter):
    """fix wrong space insert after OCR

    :param string: the string to fix.
    :param letter: string, the letter to check.
    :return: string
    """
    res = string

    if (letter + " ") in res:
        for word in get_csv_words(letters_maps_directory + letter + '_space_upp_plural.csv'):
            res = remove_space_from_word(res, word, True, True)

        for word in get_csv_words(letters_maps_directory + letter + '_space_upp.csv'):
            res = remove_space_from_word(res, word, True, False)

        for word in get_csv_words(letters_maps_directory + letter + '_space.csv'):
            res = remove_space_from_word(res, word, False, False)

        for word in get_csv_words(letters_maps_directory + letter + '_space_plural.csv'):
            res = remove_space_from_word(res, word, False, True)

    # if (letter + " ") in res:
        # print("Unknown " + letter + "_ : " + res.replace("\n", ""))

    return res


def fix_common_misspells(string):
    """Hardcoded fixes of many errors

    :param string: the string to fix.
    :return: string
    """
    res = string

    for error in get_csv_words_map(strings_maps_directory + 'common_misspells.csv'):
        regex = r"\b" + error[0] + r"\b"
        res = re.sub(r"" + regex, error[1], res)

    return res


def fix_numbers(string):
    """Fix spaces in numbers

    :param string: the string to fix.
    :return: string
    """
    res = string

    if re.match("\d\s", string):
        print("found number : " + re.sub(r"(?<=\d)\s(?=[\d\.:,-])", "", string))

    return res

