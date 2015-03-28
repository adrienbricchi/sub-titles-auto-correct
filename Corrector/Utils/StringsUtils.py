#!/usr/bin/python3
# -*-coding:utf8 -*


import re                                                   # regular expression
import csv
import subprocess
import os


strings_maps_directory = os.path.dirname(os.path.abspath(__file__)) + '/StringsMaps/'
letters_maps_directory = strings_maps_directory + 'LettersMaps/'
lower_case = r"[a-zàâäçéèêëîïôöùûü]"
upper_case = r"[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜ]"
file_cache = {}


# region Utils


def print_if_found_char(tag, string, char, language):
    """logs warn if the string contains given char

    :param tag: a prefix to the printed string.
    :param string: the string to check.
    :param char: the char to log
    :param char: the language to check
    :return:
    """
    if char in string:
        to_check = string
        to_check = re.sub(r"(\b[^" + char + r"\s]+\b)", "", to_check)
        to_check = re.sub(r"\W", r" ", to_check)

        for word in get_csv_words_with_language(letters_maps_directory + char + '_trusted.csv', language):
            to_check = re.sub(r"\b([" + word[:1] + word[:1].upper() + r"]" + word[1:] + r")\b", "", to_check)

        if re.match(upper_case, char):
            to_check = re.sub(r"\b(" + upper_case + r"+" + char + upper_case + r"*)\b", "", to_check)
            to_check = re.sub(r"\b(" + upper_case + r"*" + char + upper_case + r"+)\b", "", to_check)

        if char in to_check:
            print("Found " + char + " in " + (tag + " : " if len(tag) > 0 else ": ") + string.replace("\n", ""))

    return


def print_single_letters(string):
    """print single letters, ignoring A-a-I.

    :param string: the string to check.
    :return:
    """
    if re.search(r"\b[b-zB-HJ-Z]\b", string):
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


def is_time_code(text):
    """True if not matching the "00:01:02,003 --> 00:01:05,000"

    :param text: string, the string to test.
    :return: boolean
    """
    return re.match(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$", text)


def is_index(lines, index):
    """True if is a simple number followed by time code

    :param lines: file strings
    :param index: the line index to test
    :return: boolean
    """
    if not re.match(r"^\d+$", lines[index]):
        return False

    if index == len(lines):
        return False

    if is_time_code(lines[index + 1]):
        return True

    return False


def is_text_line(lines, index):
    """True if not empty, not a number, and not a time code

    :param lines: file strings
    :param index: the line index to test
    :return: boolean
    """
    if lines[index] == "":
        return False

    if is_index(lines, index):
        return False

    if is_time_code(lines[index]):
        return False

    return True


def get_csv_words_with_language(csv_file_path, language):
    """Safe file word list, gets regular and localized csv content

    :param csv_file_path: source path
    :param language: language csv file suffix
    :return: list of strings, or empty list
    """
    localized_csv_path = re.sub(r"\.csv$", "." + language + ".csv", csv_file_path)

    result_list = []
    result_list += get_csv_words(csv_file_path)
    result_list += get_csv_words(localized_csv_path)

    return result_list


def get_csv_words(csv_file_path):
    """Safe file word list

    :param csv_file_path: source path
    :return: list of strings, or empty list
    """
    result_list = []

    if csv_file_path in file_cache:
        return file_cache[csv_file_path]

    if os.path.isfile(csv_file_path):
        with open(csv_file_path, newline='') as csv_file:
            csv_file_reader = csv.reader(csv_file, delimiter=':', quotechar='|')
            for word in csv_file_reader:
                result_list.append(word[0])

    file_cache[csv_file_path] = result_list
    return result_list


def get_csv_words_map_with_language(csv_file_path, language):
    """Safe file word list, gets regular and localized csv content

    :param csv_file_path: source path
    :param language: language csv file suffix
    :return: list of strings arrays, or empty list
    """
    localized_csv_path = re.sub(r"\.csv$", "." + language + ".csv", csv_file_path)

    result_list = []
    result_list += get_csv_words_map(csv_file_path)
    result_list += get_csv_words_map(localized_csv_path)

    return result_list


def get_csv_words_map(csv_file_path):
    """Safe file list

    :param csv_file_path: source path
    :return: list of strings arrays, or empty list
    """
    result_list = []

    if csv_file_path in file_cache:
        return file_cache[csv_file_path]

    if os.path.isfile(csv_file_path):
        with open(csv_file_path, newline='') as csv_file:
            csv_file_reader = csv.reader(csv_file, delimiter=':', quotechar='|')
            for words in csv_file_reader:
                result_list.append(words)

    file_cache[csv_file_path] = result_list
    return result_list


def launch_ms_word_spell_check(path, language):
    command_line = ""

    office2010_location = "C:\Program Files\Microsoft Office\Office14\Winword.exe"
    if os.path.isfile(office2010_location):
        command_line += office2010_location

    if command_line == "":
        print("MSOffice is missing, or no known MSOffice found")
        return

    command_line += ' /t "' + path + '"'

    if language == "fr":
        command_line += ' /mSrtFrSpellCheck'
    elif language == "eng":
        command_line += ' /mSrtEngSpellCheck'
    else:
        command_line += ' /mSrtSpellCheck'

    print(command_line)
    subprocess.call(command_line)
    return


def force_string_size(string, size):
    """Adds spaces to given string, until it matches the wanted size.

    :param string: the string to transform.
    :param size: the size to match.
    :return: string
    """
    result = string
    result += " " * (size - len(string.replace("\n", "")))
    return result


# endregion Utils


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


def fix_quotes(line, language):
    """ '' => ", and fix spaces.
    Add a space after the three dots, if there isn't, and if isn't before a linebreak

    :param line: the string to fix.
    :return: string
    """
    line = line.replace("' '", "\"")
    line = line.replace("''", "\"")

    if re.search("\s'", line):
        for word in get_csv_words_with_language(strings_maps_directory + 'quote_word_trusted.csv', language):
            line = re.sub(r"\s'" + word + r"\b", "'" + word, line)

    if re.search("'\s", line):
        for word in get_csv_words_with_language(strings_maps_directory + 'word_quote_trusted.csv', language):
            line = re.sub(r"\b" + word + r"'\s", word + "'", line)

    if re.search("'\s", line):
        print("Unknown '_ : " + line.replace("\n", ""))
    if re.search("\s'", line):
        print("Unknown _' : " + line.replace("\n", ""))

    return line


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


def fix_letter_followed_by_space(line, letter, language):
    """fix wrong space insert after OCR

    :param line: the string to fix.
    :param letter: string, the letter to check.
    :return: string
    """
    res = line

    if (letter + " ") in res:
        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_upp_plural.csv', language):
            res = remove_space_from_word(res, word, True, True)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_upp.csv', language):
            res = remove_space_from_word(res, word, True, False)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space.csv', language):
            res = remove_space_from_word(res, word, False, False)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_plural.csv', language):
            res = remove_space_from_word(res, word, False, True)

    if letter + " " in line:
        to_check = line.replace("\n", "")
        to_check = re.sub(r"\b(\w*[^" + letter + r")\s])\b", "", to_check)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_trusted.csv', language):
            to_check = re.sub(r"\b([" + word[:1] + word[:1].upper() + r"]" + word[1:] + r")\b", "", to_check)

        if letter + " " in to_check:
            print("Unknown " + letter + "_ : " + line.replace("\n", ""))

    return res


def fix_common_errors(string):
    """Hardcoded fixes that can't be set in common mispells

    :param string: the string to fix.
    :return: string
    """
    string = re.sub(r"<i>(\s*)</i>", r"\1", string)
    string = re.sub(r"</i>(\s*)<i>", r"\1", string)

    return string


def fix_common_misspells(string, language):
    """Hardcoded fixes of many errors

    :param string: the string to fix.
    :return: string
    """
    for error in get_csv_words_map_with_language(strings_maps_directory + 'common_misspells.csv', language):
        regex = r"\b" + error[0] + r"\b"
        string = re.sub(r"" + regex, error[1], string)

    return string


def fix_numbers(string):
    """Fix spaces in numbers

    :param string: the string to fix.
    :return: string
    """
    string = re.sub(r"(?<=\d)\s(?=[\s\d])", "", string)

    for word in get_csv_words(strings_maps_directory + 'number_succeeded_by_space_trusted.csv'):
        string = re.sub(r"(?<=\d)\s(?=" + word + r"\b)", "", string)

    if re.search(r"\d\d\d\d\d", string):
        print("Big number : " + string.replace("\n", ""))

    while re.search(r"\b\d+\d\d\d\d\b", string):
        string = re.sub(r"\b(\d+\d)(\d\d\d)\b", r"\1 \2", string)

    return string


def fix_capital_i_to_l(string):
    """Checks for wrong capital I and switch them with l

    Will fix :
       *  aIb      :   alb
       *  abI      :   abl
       *  AIb      :   Alb
       *  aIIIb    :   alllb
       *  abIII    :   ablII

    :param string: the string to fix.
    :return: string
    """
    while re.search(r"" + lower_case + "I", string):
        string = re.sub(r"(?<=" + lower_case + r")I", "l", string)

    while re.search(r"" + upper_case + "I" + lower_case, string):
        string = re.sub(r"(?<=" + upper_case + r")I(?=" + lower_case + r")", "l", string)

    while re.search(r"" + lower_case + r"\sI" + lower_case, string):
        string = re.sub(r"(?<=" + lower_case + r"\s)I(?=" + lower_case + r")", "l", string)

    while re.search(r",\sI" + lower_case, string):
        string = re.sub(r"(?<=,\s)I(?=" + lower_case + r")", "l", string)

    return string


def fix_l_to_capital_i(string):
    """Checks for wrong capital I and switch them with l

    Will fix :
       *  -AlB      :   - AIB
       *  -AllB     :   - AIIB

    :param string: the string to fix.
    :return: string
    """
    while re.search(r"" + upper_case + "l+" + upper_case, string):
        string = re.sub(r"(?<=" + upper_case + r")l(?=l*" + upper_case + r")", "I", string)

    return string