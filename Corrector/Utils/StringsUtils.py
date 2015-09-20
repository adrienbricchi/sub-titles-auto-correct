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

shell_color_header = '\033[95m'
shell_color_ok_blue = '\033[94m'
shell_color_ok_green = '\033[92m'
shell_color_warning = '\033[93m'
shell_color_fail = '\033[91m'
shell_color_end = '\033[0m'
shell_color_bold = '\033[1m'
shell_color_underline = '\033[4m'


# region Utils


def find_words_with_char(string, char, language):
    """getting words with asked char, in given string.

    :param string: the string to check.
    :param char: the char to log
    :param char: the language to check
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
        csv_file = letters_maps_directory + char + '_trusted.csv'
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
        string = string.replace(word, shell_color_warning + word + shell_color_end)

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


def put_csv_word(csv_file_path, key, value):
    """Concat line at the end of CSV file.

    :param csv_file_path: source path
    :param key: can't be null
    :param value: None for single column CSV
    """
    file_cache.pop(csv_file_path, None)

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
        prompt = input("Found " + shell_color_warning + word + shell_color_end + " : ")

        if prompt == ":x":
            trusted_file_path = letters_maps_directory + re.sub(r"\.csv$", "." + language + ".csv", trusted_file_path)
            put_csv_word(trusted_file_path, word, None)
        elif prompt == ":x!":
            trusted_file_path = letters_maps_directory + trusted_file_path
            put_csv_word(trusted_file_path, word, None)
        elif prompt == ":q":
            print("Skipped...")
        else:
            string = string.replace(word, prompt)
            prompt_should_register = input("    Register? : ")

            if prompt_should_register == ":x":
                common_misspells_file_path = strings_maps_directory + "common_misspells." + language + ".csv"
                put_csv_word(common_misspells_file_path, word, prompt)
            elif prompt_should_register == ":x!":
                common_misspells_file_path = strings_maps_directory + "common_misspells.csv"
                put_csv_word(common_misspells_file_path, word, prompt)

    return string


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


def remove_all_uppercase_words(array):
    """Simple uppercase filter on given array.

    :param array: the array to fix.
    :return: array
    """
    return [word for word in array if not re.match(r"^(" + upper_case + r"){3,}$", word)]


# endregion Utils


# region Single line


def fix_accentuated_capital_a(string):
    """Prompt to switch A into À

    :param string: the string to check.
    :return: string
    """
    if re.search(r"\bA\b", string):
        for matching_range in [m.span() for m in re.finditer(r"\bA\b", string)]:

            colour_string = string[:matching_range[0]]
            colour_string += shell_color_warning + "A" + shell_color_end
            colour_string += string[matching_range[1]:]

            prompt = input("Found A in \"" + colour_string.replace("\n", "") + "\" : ")
            if prompt == ":x":
                string = colour_string.replace(shell_color_warning + "A" + shell_color_end, "À")

    return string


def fix_common_errors(string):
    """Hardcoded fixes that can't be set in common misspells.

    :param string: the string to check.
    :return: string
    """
    string = re.sub(r"(?<=\d)\s*([hH])\s*(?=\d)", r"\1", string)
    string = string.replace("- \\", "- ")
    string = string.replace(" )", ")")
    string = string.replace("( ", "(")
    string = string.replace(" ]", "]")
    string = string.replace("[ ", "[")

    return string


def fix_punctuation_errors(string, language):
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

    # if re.search("'\s", line):
    #     print("Unknown '_ : " + line.replace("\n", ""))
    # if re.search("\s'", line):
    #     print("Unknown _' : " + line.replace("\n", ""))

    return line


def fix_question_marks(string):
    """ *? => *_?
    Add a space after the three dots, if there isn't, and if isn't before a linebreak

    :param string: the string to fix.
    :return: string
    """

    if "?" in string:
        string = re.sub(r"(?<!\s)\?", " ?", string)
        string = re.sub(r"(?<=[!\?])\s+(?=[!\?])", "", string)

    return string


def fix_exclamation_marks(string):
    """ *! => *_!

    :param string: the string to fix.
    :return: string
    """
    res = string

    if "!" in string:
        res = re.sub(r"(?<!\s)!", " !", res)

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
    :return: string
    """
    if (letter + " ") in line:
        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_upp_plural.csv', language):
            line = remove_space_from_word(line, word, True, True)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_upp.csv', language):
            line = remove_space_from_word(line, word, True, False)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space.csv', language):
            line = remove_space_from_word(line, word, False, False)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_plural.csv', language):
            line = remove_space_from_word(line, word, False, True)

    if letter + " " in line:
        line_to_print = line.replace("\n", "")
        to_check = line.replace("\n", "")
        to_check = re.sub(r"\b(\w*[^" + letter + r")\s])\b", "", to_check)

        for word in get_csv_words_with_language(letters_maps_directory + letter + '_space_trusted.csv', language):
            to_check = re.sub(r"\b([" + word[:1] + word[:1].upper() + r"]" + word[1:] + r")\b", "", to_check)

        # Print colored char
        if letter + " " in to_check:
            line_to_print = re.sub(r"(\w*" + letter + r")(?=\s)", shell_color_warning + r"\1" + shell_color_end, line_to_print)
            print("Unknown " + letter + "_ : " + line_to_print)

    return line


def fix_italic_tag_errors(string):
    """Fixes useless tags, and wrong spaces around.

    :param string: the string to fix.
    :return: string
    """
    string = re.sub(r"<i>(\s*)</i>", r"\1", string)
    string = re.sub(r"</i>(\s*)<i>", r"\1", string)
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
    string = re.sub(r"(?<=\d)\s:\s(?=\d)", ":", string)

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

    while re.search(r"" + "l+" + upper_case + upper_case, string):
        string = re.sub(r"l(?=" + upper_case + r"{2})", "I", string)

    return string


def fix_acronyms(string):
    """fixes spaces after dots on acronyms.

    :param string: the string to fix.
    :return: string
    """
    string = re.sub(r"(?<=\b\w\.)(\s*)(?=\w\.)", "", string)

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
    for i in range(0, len(strings) - 1):
        if strings[i].endswith("</i>\n") and strings[i+1].startswith("<i>"):
            strings[i] = strings[i][:-5] + "\n"
            strings[i+1] = strings[i+1][3:]

    return strings


def fix_missing_dialog_hyphen(strings):
    """Adds a dialog hyphen on the first line, if the following has one.

    :param strings: an array of strings to fix.
    :return: string array
    """
    start_with_hyphen_regex = r"^(<i>)?\s*-(?!-).*$"

    if len(strings) == 2:
        if re.match(start_with_hyphen_regex, strings[1]):
            if not re.match(start_with_hyphen_regex, strings[0]):
                strings[0] = "- " + strings[0]

    return strings


def fix_double_quotes_errors(strings):
    """Checks even number of double quotes.

    :param strings: an array of strings to fix.
    :return: string array
    """
    count = 0
    for string in strings:
        count += len(re.findall(r"\"", string))

    if (count % 2) == 1:
        last_string_index = len(strings) - 1

        if strings[0].startswith("\""):
            last_string_length = len(strings[last_string_index])
            strings[last_string_index] = strings[last_string_index][:last_string_length - 1] + "\"\n"
        elif strings[last_string_index].endswith("\"\n"):
            strings[0] = "\"" + strings[0]

    return strings


# endregion Multi-lines


def fix_multiline_errors(lines, current_language):
    """Every fixes defined here.

    :param lines: the lines to fix.
    :return: string
    """

    lines = fix_double_quotes_errors(lines)

    if len(lines) == 1:
        return lines

    lines = fix_empty_lines(lines)
    lines = fix_redundant_italic_tag(lines)
    lines = fix_missing_dialog_hyphen(lines)

    return lines


def fix_single_line_errors(string, current_language):
    """Every fixes defined here.

    :param string: the string to fix.
    :return: string
    """
    string = fix_common_errors(string)
    string = fix_punctuation_errors(string, current_language)
    string = fix_numbers(string)
    string = fix_italic_tag_errors(string)
    string = fix_colon(string)
    string = fix_capital_i_to_l(string)
    string = fix_l_to_capital_i(string)
    string = fix_acronyms(string)
    string = fix_common_misspells(string, current_language)
    string = fix_letter_followed_by_space(string, "f", current_language)
    string = fix_letter_followed_by_space(string, "W", current_language)
    string = fix_letter_followed_by_space(string, "C", current_language)
    string = fix_letter_followed_by_space(string, "G", current_language)
    string = fix_letter_followed_by_space(string, "Z", current_language)
    string = fix_letter_followed_by_space(string, "V", current_language)
    string = fix_quotes(string, current_language)
    string = fix_question_marks(string)
    string = fix_degree_symbol(string)
    string = fix_exclamation_marks(string)
    string = fix_dialog_hyphen(string)

    return string
