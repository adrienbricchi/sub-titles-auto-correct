#!/usr/bin/python3
# -*-coding:utf8 -*


import re                                                   # regular expression


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
        for word in quote_word_list:
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
        if letter in letter_space_upp_plural_list:
            for word in letter_space_upp_plural_list[letter]:
                res = remove_space_from_word(res, word, True, True)

        if letter in letter_space_upp_list:
            for word in letter_space_upp_list[letter]:
                res = remove_space_from_word(res, word, True, False)

        if letter in letter_space_list:
            for word in letter_space_list[letter]:
                res = remove_space_from_word(res, word, False, False)

        if letter in letter_space_plural_list:
            for word in letter_space_plural_list[letter]:
                res = remove_space_from_word(res, word, False, True)

    # if (letter + " ") in res :
    #     print("Unknown " + letter + "_ : " + res.replace("\n", ""))

    return res


def fix_common_misspells(string):
    """Hardcoded fixes of many errors

    :param string: the string to fix.
    :return: string
    """
    res = string

    for error in recurent_mispells:
        regex = r"\b" + error + r"\b"
        res = re.sub(r"" + regex, recurent_mispells[error], res)

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


# region Common errors


recurent_mispells = {"Seinfelf" : "Seinfeld",                   "Everybofy" : "Everybody",
                     "Raymonf" : "Raymond",                     "Alreafy" : "Already",
                     "Wilf Wilf West" : "Wild Wild West",       "Richarfs" : "Richards",
                     "Rockforf" : "Rockford",                   "Hollywoof" : "Hollywood",
                     "J AG" : "JAG",                            "Anf" : "And",
                     "Touchef" : "Touched",                     "Maf About You" : "Mad About You",
                     "3rf Rock from" : "3rd Rock from",         "Deaf Again" : "Dead Again",
                     "Provifence" : "Providence",               "The Mutef Heart" : "The Muted Heart",
                     "Heaf of State" : "Head of State",         "anf" : "and",
                     "Accorfing" : "According",                 "Marbleheaf Manor" : "Marblehead Manor",
                     "Ef Woof" : "Ed Wood",                     "The Lanf Before Time" : "The Land Before Time",
                     "The Prife of" : "The Pride of",           "Methof & Ref" : "Method & Red",
                     "Colf Case" : "Cold Case",                 "Davif Letterman" : "David Letterman",
                     "The Bolf and" : "The Bold and",           "Baf Boys" : "Bad Boys",
                     "Cagef Birf" : "Caged Bird",               "Hanf That Rocks the Crafle" : "Hand That Rocks the Cradle",
                     "War of the Worlfs" : "War of the Worlds", "Arrestef Development" : "Arrested Development",
                     "Harolf and Maufe" : "Harold and Maude",   "Frienfs" : "Friends",
                     "Islanf" : "Island",                       "Weffing" : "Wedding",
                     "Worlf" : "World",                         "Minf" : "Mind"}

quote_word_list =     ["ll", "s", "m", "t", "re", "ve"]

number_succeeded_by_space_list =     ["h", "\.", ",", "min", "-", ":", "kg", "g", "l", "'", "th", "cd", "st"
                                      "rd", "ème", "cd", "er", "ère"]


# endregion Common errors


# region Letter followed by space


C_space_upp_plural_list = []

C_space_upp_list =        []

C_space_plural_list =     []

C_space_list =            ["C yphers", "C ynthia"]

f_space_upp_plural_list = ["inf ormation", "eff ect", "ref er", "suff er", "eff ect", "lif e", "perf orming",
                          "perf ormer", "inf orm", "ref erence", "prof essional", "diff erent", "inf ection",
                          "perf ormance", "off er", "coff ee", "comf ortable", "off ender", "coff eemaker",
                          "caff eine", "def ense", "chauff eur", "inf o", "unif orm", "aff ect", "off ensive",
                          "lif etime", "aff ection", "knif e", "perf ect", "rif e", "misf ortune", "perf orm",
                          "aff ord"]

f_space_upp_list =        ["bef ore", "ref erred", "saf e", "ref erring", "ref erenced", "perf ormed", "off ered",
                           "pref erred", "inf ected", "def ormities", "saf ety", "unf ortunately", "def eated",
                           "theref ore", "aff ected", "transf ormed", "saf ely", "diff ered"]

f_space_plural_list =     ["f eeling", "f eature", "f eel", "f ounding", "f ootage", "f ormer", "f ermentation",
                           "f ood", "f ollow", "f ound", "f orm", "f oreign", "f etishist", "Conf ederate", "f ence",
                           "f emale", "f eaturing", "f oul", "f ellow", "f ounder", "f ee", "f olk", "f ormat",
                           "f orce"]

f_space_list =            ["Leif er", "f or", "f oot", "f eet", "f ollowing", "Radf ord", "Schaff er", "f our",
                           "Seinf eld", "Calif ornia", "f ew", "f ounded", "f eatured", "wif e", "f ourth", "Bedf ord",
                           "Phif er", "Mulf ord", "Movief one", "Jennif er", "f ocusing", "f elt", "f ormulated",
                           "f ormed"]

G_space_upp_plural_list = []

G_space_upp_list =        []

G_space_plural_list =     ["G irl", "G iant"]

G_space_list =            ["G ilmore", "G illigan", "G igolo"]


letter_space_upp_plural_list =  {"C" : C_space_upp_plural_list,
                                 "f" : f_space_upp_plural_list,
                                 "G" : G_space_upp_plural_list}

letter_space_upp_list =         {"C" : C_space_upp_list,
                                 "f" : f_space_upp_list,
                                 "G" : G_space_upp_list}

letter_space_plural_list =      {"C" : C_space_plural_list,
                                 "f" : f_space_plural_list,
                                 "G" : G_space_plural_list}

letter_space_list =             {"C" : C_space_list,
                                 "f" : f_space_list,
                                 "G" : G_space_list}


# endregion Letter followed by space