#!/usr/bin/python3
# -*-coding:utf8 -*

import re
import csv
import subprocess
import os
from Corrector.Utils import Consts


STRINGS_MAPS_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + '/StringsMaps/'
LETTERS_MAPS_DIRECTORY = STRINGS_MAPS_DIRECTORY + 'LettersMaps/'
LOWER_CASE = r"[a-zàâäçéèêëîïôöùûü]"
UPPER_CASE = r"[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜ]"
START_WITH_HYPHEN_REGEX = r"^((?:<i>\s*|\"\s*)*)-(?!\s*-)\s*(.*)"
ENDS_WITH_HYPHEN_REGEX = r"^(.*)\"((?:</i>)?)$"
SENTENCE_START_REGEX = r"^((?:<i>|-\s*)*)(.*)"
SDH_CHARS = r"[A-Z0-9\s,()\.!\?\[\]-]{2,}"
ENDS_WITHOUT_ENDING_SENTENCE_REGEX = r".*[a-zA-Z]$"
FILE_CACHE = {}

SHELL_COLOR_HEADER = '\033[95m'
SHELL_COLOR_OK_BLUE = '\033[94m'
SHELL_COLOR_OK_GREEN = '\033[92m'
SHELL_COLOR_WARNING = '\033[93m'
SHELL_COLOR_FAIL = '\033[91m'
SHELL_COLOR_END = '\033[0m'
SHELL_COLOR_BOLD = '\033[1m'
SHELL_COLOR_UNDERLINE = '\033[4m'


# region Utils


def find_words_with_char(string, char, language):
    """getting words with asked char, in given string.

    :param string: the string to check.
    :param char: the char to log
    :param language: current language correction
    :return: an array (maybe empty)
    """
    result = []

    if char in string:
        # Filtering everything but alphabetical chars
        string = re.sub(r"(\b[^" + char + r"\s]+\b)", "", string)
        string = re.sub(r"\W", " ", string)
        result = string.split()

        # Filtering non-matching words
        result = [value for value in result if char in value]

        # Filtering trusted words
        csv_file = LETTERS_MAPS_DIRECTORY + char + '_trusted.csv'
        for word in get_csv_words_with_language(csv_file, language):
            result = [value for value in result if value != word]
            result = [value for value in result if value != (word[:1] + word[:1])]

    return result


def warns_list_words(string, array):
    """Colors the given words in the given string.

    :param string: the string to check
    :param array: words to warn
    :return:
    """
    for word in array:
        string = string.replace(word, SHELL_COLOR_WARNING + word + SHELL_COLOR_END)

    return string


def print_single_letters(string):
    """Print single letters, ignoring A-a-I.

    :param string: the string to check.
    :return: string
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
    :param language: current language correction
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

    if csv_file_path in FILE_CACHE:
        return FILE_CACHE[csv_file_path]

    if os.path.isfile(csv_file_path):
        with open(csv_file_path, newline='') as csv_file:
            csv_file_reader = csv.reader(csv_file, delimiter=':', quotechar='|')
            for word in csv_file_reader:
                result_list.append(word[0])

    FILE_CACHE[csv_file_path] = result_list
    return result_list


def get_csv_words_map_with_language(csv_file_path, language):
    """Safe file word list, gets regular and localized csv content

    :param csv_file_path: source path
    :param language: current language correction
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

    if csv_file_path in FILE_CACHE:
        return FILE_CACHE[csv_file_path]

    if os.path.isfile(csv_file_path):
        with open(csv_file_path, newline='') as csv_file:
            csv_file_reader = csv.reader(csv_file, delimiter=':', quotechar='|')
            for words in csv_file_reader:
                result_list.append(words)

    FILE_CACHE[csv_file_path] = result_list
    return result_list


def put_csv_word(csv_file_path, key, value):
    """Concat line at the end of CSV file.

    :param csv_file_path: source path
    :param key: can't be null
    :param value: None for single column CSV
    """
    FILE_CACHE.pop(csv_file_path, None)

    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=':', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if not value:
            writer.writerow([key])
        else:
            writer.writerow([key, value])
    return


def ask_for_correction(string, array, trusted_file_path, language):
    """Prompt for a correction.
    :q  - Ignore current line
    :x  - Ignore and add to language csv file
    :x! - Ignore and add to general csv file

    :param string: the string to fix
    :param array: errors to print
    :param trusted_file_path: path to trusted csv
    :param language: current language
    :return: fixed string
    """
    if len(array) > 0:
        print(warns_list_words(string.replace("\n", ""), array))

    for word in array:
        prompt = input("Found " + SHELL_COLOR_WARNING + word + SHELL_COLOR_END + " : ")

        if prompt == ":x":
            trusted_file_path = LETTERS_MAPS_DIRECTORY + re.sub(r"\.csv$", "." + language + ".csv", trusted_file_path)
            put_csv_word(trusted_file_path, word, None)
        elif prompt == ":x!":
            trusted_file_path = LETTERS_MAPS_DIRECTORY + trusted_file_path
            put_csv_word(trusted_file_path, word, None)
        elif prompt == ":q":
            print("Skipped...")
        else:
            string = string.replace(word, prompt)
            prompt_should_register = input("    Register? : ")

            if prompt_should_register == ":x":
                common_misspells_file_path = STRINGS_MAPS_DIRECTORY + "common_misspells." + language + ".csv"
                put_csv_word(common_misspells_file_path, word, prompt)
            elif prompt_should_register == ":x!":
                common_misspells_file_path = STRINGS_MAPS_DIRECTORY + "common_misspells.csv"
                put_csv_word(common_misspells_file_path, word, prompt)

    return string


def launch_ms_word_spell_check(path, language):
    command_line = ""

    office2010_location = 'C:\Program Files\Microsoft Office\Office14\Winword.exe'
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


def remove_all_uppercase_words(array):
    """Simple uppercase filter on given array.

    :param array: the array to fix.
    :return: array
    """
    return [word for word in array if not re.match(r"^(" + UPPER_CASE + r"){3,}$", word)]


# endregion Utils


# region Single line


def fix_accentuated_capital_a(string):
    """Prompt to switch A into À

    :param string: the string to check.
    :return: string
    """
    matches = list(re.finditer(r"\bA\b", string))
    for i in range(0, len(matches)):
        match = matches[i]
        colour_string = string[:match.start()] + SHELL_COLOR_WARNING + "A" + SHELL_COLOR_END + string[match.end():]
        prompt = input("Found A in \"" + colour_string.replace("\n", "") + "\" : ")
        if prompt == ":x":
            string = colour_string.replace(SHELL_COLOR_WARNING + "A" + SHELL_COLOR_END, "À")

    return string


def fix_common_errors(string):
    """Hardcoded fixes that can't be set in common misspells.

    :param string: the string to check.
    :return: string
    """
    string = re.sub(r"(?<=\d)\s*([hH])\s*(?=\d)", r"\1", string)
    string = string.replace("- \\", "- ")
    string = string.replace("’", "'")
    string = string.replace(" )", ")")
    string = string.replace("( ", "(")
    string = string.replace(" ]", "]")
    string = string.replace("[ ", "[")

    return string


def fix_punctuation_errors(string):
    """Add a space after the three dots, before or after a dot, etc

    :param string: the string to fix.
    :return: string
    """
    string = string.replace(". . .", "...")
    string = string.replace(".. .", "...")
    string = string.replace(". ..", "...")
    string = re.sub(r"\.\s*\"$", ".\"", string)

    if "..." in string:
        string = re.sub(r"\.\.\.(?=\w)", "... ", string)
        string = re.sub(r"\.\.\.\.+", "...", string)

    string = string.replace("‘", "'")

    if "--" in string:
        string = re.sub(r"\s*--", " --", string)

    return string


def fix_quotes(line, language):
    """ '' => ", and fix spaces.
    Add a space after the three dots, if there isn't, and if isn't before a linebreak

    :param line: the string to fix.
    :param language: current language correction
    :return: string
    """
    line = line.replace("' '", "\"")
    line = line.replace("''", "\"")
    line = line.replace("‘", "'")
    line = line.replace("’", "'")

    if re.search("\s'", line):
        for word in get_csv_words_with_language(STRINGS_MAPS_DIRECTORY + 'quote_word_trusted.csv', language):
            line = re.sub(r"\s'" + word + r"\b", "'" + word, line)

    if re.search("'\s", line):
        for word in get_csv_words_with_language(STRINGS_MAPS_DIRECTORY + 'word_quote_trusted.csv', language):
            line = re.sub(r"\b" + word + r"'\s", word + "'", line)

    # if re.search("'\s", line):
    #     print("Unknown '_ : " + line.replace("\n", ""))
    # if re.search("\s'", line):
    #     print("Unknown _' : " + line.replace("\n", ""))

    return line


def fix_punctuation_spaces(string):
    """ Add needed spaces around "?" and "!"

    :param string: the string to fix.
    :return: string
    """
    if "?" in string or "!" in string:
        string = re.sub(r"(?<![\?!\s])([\?!])", r" \1", string)  # Space before
        string = re.sub(r"([\?!])(?=[\w\('-])", r"\1 ", string)  # Space after
        string = re.sub(r"(?<=[\?!])\s+(?=[!\?])", "", string)  # Space between

    return string


def fix_dialog_hyphen(string):
    """Add a space after the hyphen at the beginning of a line.

    Will fix :
       *  -text       :   - text
       *  -"text      :   - "text
       *  <i>-text    :   <i>- text
       *  -<i>text    :   - <i>text
       *  "-text      :   "- text
       *  "-... text  :   "- ... text
       *  "--text     :   "--text

    :param string: the string to fix.
    :return: string
    """
    res = re.sub(r"^(\s*|\"|<i>)-(?!\s|-)", r"\1- ", string)
    return res


def fix_letter_followed_by_space(line, letter, language):
    """fix wrong space insert after OCR

    :param line: the string to fix.
    :param letter: string, the letter to check.
    :param language: current language correction
    :return: string
    """
    if (letter + " ") in line:
        for word in get_csv_words_with_language(LETTERS_MAPS_DIRECTORY + letter + '_space_upp_plural.csv', language):
            line = remove_space_from_word(line, word, True, True)

        for word in get_csv_words_with_language(LETTERS_MAPS_DIRECTORY + letter + '_space_upp.csv', language):
            line = remove_space_from_word(line, word, True, False)

        for word in get_csv_words_with_language(LETTERS_MAPS_DIRECTORY + letter + '_space.csv', language):
            line = remove_space_from_word(line, word, False, False)

        for word in get_csv_words_with_language(LETTERS_MAPS_DIRECTORY + letter + '_space_plural.csv', language):
            line = remove_space_from_word(line, word, False, True)

    if letter + " " in line:
        line_to_print = line.replace("\n", "")
        to_check = line.replace("\n", "")
        to_check = re.sub(r"\b(\w*[^" + letter + r")\s])\b", "", to_check)

        for word in get_csv_words_with_language(LETTERS_MAPS_DIRECTORY + letter + '_space_trusted.csv', language):
            to_check = re.sub(r"\b([" + word[:1] + word[:1].upper() + r"]" + word[1:] + r")\b", "", to_check)

        # Print colored char
        if letter + " " in to_check:
            line_to_print = re.sub(r"(\w*" + letter + r")(?=\s)", SHELL_COLOR_WARNING + r"\1" + SHELL_COLOR_END,
                                   line_to_print)
            print("Unknown " + letter + "_ : " + line_to_print)

    return line


def fix_italic_tag_errors(string):
    """Fixes useless tags, and wrong spaces around.

    :param string: the string to fix.
    :return: string
    """
    string = string.replace("<i> ", " <i>")
    string = string.replace(" <\i>", "<\i> ")
    string = string.replace("<\i>-<i>", "-")
    string = string.replace("<i>-</i>", "-")
    string = re.sub(r"\s+</i>$", "</i>", string)
    string = re.sub(r"\s*\"\s*</i>$", "\"</i>", string)

    return string


def fix_colon(string):
    """Fixes spaces around colon.

    :param string: the string to fix.
    :return: string
    """
    string = re.sub(r"(?<=\w):(?=\w)", " : ", string)
    string = re.sub(r"(?<=\w):", " :", string)
    string = re.sub(r":(?=\w)", ": ", string)
    string = re.sub(r"(?<=\d)\s*:\s*(?=\d)", ":", string)

    return string


def fix_common_misspells(string, language):
    """Hardcoded fixes of many errors

    :param string: the string to fix.
    :param language: current language correction
    :return: string
    """
    for error in get_csv_words_map_with_language(STRINGS_MAPS_DIRECTORY + 'common_misspells.csv', language):
        regex = r"\b" + error[0] + r"\b"
        string = re.sub(r"" + regex, error[1], string)

    return string


def fix_numbers(string):
    """Fix spaces in numbers

    :param string: the string to fix.
    :return: string
    """
    if re.search(r"\d", string):
        string = re.sub(r"(?<=\d)\s(?=[\s\d])", "", string)

        for word in get_csv_words(STRINGS_MAPS_DIRECTORY + 'number_succeeded_by_space_trusted.csv'):
            suffix = r"\b)" if re.match(r"\w+", word) else ")"
            string = re.sub(r"(?<=\d)\s*(?=" + word + suffix, "", string)

        string = re.sub(r"(?<=\d)\s*h\s*(?=\d)", "h", string)

        if not Consts.is_unittest_exec:
            if re.search(r"\d\d\d\d\d", string):
                print("Big number : " + string.replace("\n", ""))

        while re.search(r"\b\d+\d\d\d\d\b", string):
            string = re.sub(r"\b(\d+\d)(\d\d\d)\b", r"\1 \2", string)

        # Prompt if comma or dot

        matches = list(re.finditer(r"(?<=\d)[\.,]\s*(?=\d)", string))
        prompt_results = []

        if len(matches) > 0:

            # Get fixable matches

            if Consts.is_unittest_exec:
                print("todo")
                # TODO
            else:
                for i in range(0, len(matches)):
                    result = matches[i]
                    prompt = input("Found number space in : " + string[:result.start() - 1] +
                                   SHELL_COLOR_WARNING + string[result.start() - 1:result.end() + 1] + SHELL_COLOR_END +
                                   string[result.end() + 1:].replace("\n", "") + " : ")
                    prompt_results.append(prompt == ":x")

            # Fix matches

            for i in reversed(range(0, len(prompt_results))):
                if prompt_results[i]:
                    string = string[:matches[i].start() + 1] + string[matches[i].end():]

    return string


def fix_degree_symbol(string):
    """Fix "°" symbol followed by space

    :param string: the string to fix.
    :return: string
    """

    if "°" in string:
        string = re.sub(r"(?<=\d)\s*°", "°", string)
        string = re.sub(r"(?<=\d)\s*°\s*(?=F\b)", "°", string)
        string = re.sub(r"(?<=\b[nN])\s*°\s*(?=\d)", "°", string)

    if " °" in string or "° " in string:
        print("Found ° in : " + string.replace("\n", ""))

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
    while re.search(r"" + LOWER_CASE + "I", string):
        string = re.sub(r"(?<=" + LOWER_CASE + r")I", "l", string)

    while re.search(r"" + UPPER_CASE + "I" + LOWER_CASE, string):
        string = re.sub(r"(?<=" + UPPER_CASE + r")I(?=" + LOWER_CASE + r")", "l", string)

    while re.search(r"" + LOWER_CASE + r"\sI" + LOWER_CASE, string):
        string = re.sub(r"(?<=" + LOWER_CASE + r"\s)I(?=" + LOWER_CASE + r")", "l", string)

    while re.search(r",\sI" + LOWER_CASE, string):
        string = re.sub(r"(?<=,\s)I(?=" + LOWER_CASE + r")", "l", string)

    return string


def fix_l_to_capital_i(string):
    """Checks for wrong capital I and switch them with l

    Will fix :
       *  -AlB      :   - AIB
       *  -AllB     :   - AIIB

    :param string: the string to fix.
    :return: string
    """
    while re.search(r"" + UPPER_CASE + "l+" + UPPER_CASE, string):
        string = re.sub(r"(?<=" + UPPER_CASE + r")l(?=l*" + UPPER_CASE + r")", "I", string)

    while re.search(r"" + "l+" + UPPER_CASE + UPPER_CASE, string):
        string = re.sub(r"l(?=" + UPPER_CASE + r"{2})", "I", string)

    string = re.sub(r"\bln", "In", string)
    string = re.sub(r"\blm", "Im", string)

    return string


def fix_acronyms(string):
    """fixes spaces after dots on acronyms.

    :param string: the string to fix.
    :return: string
    """
    string = re.sub(r"(?<=\b" + UPPER_CASE + r"\.)(\s*)(?=\w\.)", "", string)

    if not Consts.is_unittest_exec:
        if re.search(r"\w\.\w\.", string):
            print("Found acronym : " + string.replace("\n", ""))

    return string


# endregion Single line


# region Multi-lines


def fix_empty_lines(strings):
    """Remove empty lines of given array.

    :param strings: an array of strings to fix.
    :return: string array
    """
    filtered_strings = []

    for string in strings:
        if not re.match(r"^\s*$", string):
            filtered_strings.append(string)

    return filtered_strings


def fix_redundant_italic_tag(strings):
    """Remove <i> and </i> on followed lines.

    :param strings: an array of strings to fix.
    :return: string array
    """
    for i in range(0, len(strings)):
        strings[i] = re.sub(r"<i>(\s*)</i>", r"\1", strings[i])
        strings[i] = re.sub(r"</i>(\s*)<i>", r"\1", strings[i])

    for i in range(0, len(strings) - 1):
        if strings[i].endswith("</i>\n") and strings[i + 1].startswith("<i>"):
            strings[i] = strings[i][:-5] + "\n"
            strings[i + 1] = strings[i + 1][3:]

    return strings


def fix_useless_dialog_hyphen(strings):
    """Remove hyphens on single lines and single sentences.

    :param strings: an array of strings to fix.
    :return: string array
    """
    if len(strings) == 0:
        return strings

    if re.match(START_WITH_HYPHEN_REGEX, strings[0]):

        has_other_hyphen = False
        for i in range(1, len(strings)):
            if re.match(START_WITH_HYPHEN_REGEX, strings[i]):
                has_other_hyphen = True

        if not has_other_hyphen:
            strings[0] = re.sub(START_WITH_HYPHEN_REGEX, r"\1\2", strings[0])

    return strings


def fix_missing_dialog_hyphen(strings):
    """Adds a dialog hyphen on the first line, if the following has one.

    :param strings: an array of strings to fix.
    :return: string array
    """
    last_dialog_subtitle_index = -1
    for i in reversed(range(0, len(strings))):
        if re.match(START_WITH_HYPHEN_REGEX, strings[i]):
            last_dialog_subtitle_index = i
            break

    for i in range(0, last_dialog_subtitle_index):
        if not re.match(START_WITH_HYPHEN_REGEX, strings[i]):
            strings[i] = "- " + strings[i]
            break

    return strings


def fix_double_quotes_errors(strings):
    """Checks even number of double quotes.

    :param strings: an array of strings to fix.
    :return: string array
    """
    count = 0
    for string in strings:
        count += len(re.findall(r"\"", string))

    if (count % 2) == 0:
        return strings

    double_quote_pending = False
    for i in reversed(range(0, len(strings))):

        if re.match(ENDS_WITH_HYPHEN_REGEX, strings[i]):
            double_quote_pending = True

        if double_quote_pending and (re.match(START_WITH_HYPHEN_REGEX, strings[i]) or i == 0):
            strings[i] = re.sub(SENTENCE_START_REGEX, r'\1"\2', strings[i])
            double_quote_pending = False

    return strings


def fix_sdh_tags(strings):
    """Removes every "MAN : " tags

    :param strings: an array of strings to fix.
    :return: string array
    """
    # Character dialogs

    dialog_character_regex = r"^((?:-\s)?)(" + SDH_CHARS + r"\s*:\s*)"

    is_dialog = len(strings) > 1
    for i in range(0, len(strings)):
        if not re.match(dialog_character_regex, strings[i]):
            if not re.match(START_WITH_HYPHEN_REGEX, strings[i]):
                is_dialog = False

    for i in range(0, len(strings)):
        if is_dialog:
            strings[i] = re.sub(dialog_character_regex, "- ", strings[i])
        elif ":" in strings[i]:
            strings[i] = re.sub(dialog_character_regex, "", strings[i])

    # Sound tags

    test_string = ""
    for i in range(0, len(strings)):
        test_string += strings[i]

    test_string.replace("\n", "")
    if re.match(r"^[\[\(]" + SDH_CHARS + r"[\]\)]$", test_string):
        strings = [""]

    return strings


# endregion Multi-lines


def fix_multi_line_errors(lines):
    """Every fixes defined here.

    :param lines: the lines to fix.
    :return: string
    """

    lines = fix_double_quotes_errors(lines)

    if Consts.fix_sdh:
        lines = fix_sdh_tags(lines)

    if len(lines) == 1:
        lines = fix_useless_dialog_hyphen(lines)
    else:
        lines = fix_empty_lines(lines)
        lines = fix_redundant_italic_tag(lines)
        lines = fix_missing_dialog_hyphen(lines)

    return lines


def fix_single_line_errors(string, language):
    """Every fixes defined here.

    :param string: the string to fix.
    :param language: current language correction
    :return: string
    """
    string = fix_common_errors(string)
    string = fix_punctuation_errors(string)
    string = fix_numbers(string)
    string = fix_italic_tag_errors(string)
    string = fix_colon(string)
    string = fix_capital_i_to_l(string)
    string = fix_l_to_capital_i(string)
    string = fix_acronyms(string)
    string = fix_common_misspells(string, language)
    string = fix_letter_followed_by_space(string, "f", language)
    string = fix_letter_followed_by_space(string, "W", language)
    string = fix_letter_followed_by_space(string, "C", language)
    string = fix_letter_followed_by_space(string, "G", language)
    string = fix_letter_followed_by_space(string, "Z", language)
    string = fix_letter_followed_by_space(string, "V", language)
    string = fix_quotes(string, language)
    string = fix_punctuation_spaces(string)
    string = fix_degree_symbol(string)
    string = fix_dialog_hyphen(string)

    return string
