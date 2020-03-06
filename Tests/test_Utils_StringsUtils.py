#!/usr/bin/python3
# -*-coding:utf8 -*

# sub-titles-auto-correct
# Copyright (C) 2014-2018
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from unittest.mock import patch
from io import StringIO
import sys

from Corrector.Utils import StringsUtils
from Corrector.Utils import Consts


Consts.is_unittest_exec = True

TEST_LINES = {}
RESULT_LINES = {}
RESULT_PROMPT = {}


# noinspection SpellCheckingInspection
def populate_single_line_test_dict():

    TEST_LINES["fix_accentuated_capital_a_:x"] = ["A toi a\n", "Plop Abcdc. A.\n"]
    RESULT_LINES["fix_accentuated_capital_a_:x"] = ["À toi a\n", "Plop Abcdc. À.\n"]
    TEST_LINES["fix_accentuated_capital_a_2"] = ["A toi a\n", "Plop Abcdc. A.\n"]
    RESULT_LINES["fix_accentuated_capital_a_2"] = ["A toi a\n", "Plop Abcdc. A.\n"]
    TEST_LINES["fix_accentuated_capital_a_3"] = ["A-t-on toi a\n", "Plop Abcdc. A.\n"]
    RESULT_LINES["fix_accentuated_capital_a_3"] = ["A-t-on toi a\n", "Plop Abcdc. A.\n"]

    TEST_LINES["fix_common_errors"] = ["( Test )\n", "– [ Plop ]\n"]
    RESULT_LINES["fix_common_errors"] = ["(Test)\n", "- [Plop]\n"]

    TEST_LINES["fix_quotes"] = ["''Plop''\n", "Plop 'm O' Connor\n"]
    RESULT_LINES["fix_quotes"] = ["\"Plop\"\n", "Plop'm O'Connor\n"]

    TEST_LINES["fix_punctuation_errors"] = ["Test. . .Test.. .\n", "Plop--\n"]
    RESULT_LINES["fix_punctuation_errors"] = ["Test... Test...\n", "Plop --\n"]

    TEST_LINES["fix_punctuation_spaces"] = ["Hey! ?What ? ! ? !!\n", "Ok ! \"Line 2?\"?\n"]
    RESULT_LINES["fix_punctuation_spaces"] = ["Hey !? What ?!?!!\n", "Ok ! \"Line 2 ?\" ?\n"]

    TEST_LINES["fix_dialog_hyphen_1"] = ["-Plop\n", "--Plop\n", "-\"Plop\n"]
    RESULT_LINES["fix_dialog_hyphen_1"] = ["- Plop\n", "--Plop\n", "- \"Plop\n"]
    TEST_LINES["fix_dialog_hyphen_2"] = ["<i>-Plop\n", "\"-Plop\n", "\"-... Plop\n"]
    RESULT_LINES["fix_dialog_hyphen_2"] = ["<i>- Plop\n", "\"- Plop\n", "\"- ... Plop\n"]

    TEST_LINES["fix_letter_followed_by_space_f"] = ["chef f oreign f ollow\n"]
    RESULT_LINES["fix_letter_followed_by_space_f"] = ["chef foreign follow\n"]
    TEST_LINES["fix_letter_followed_by_space_C"] = ["TEST C ynthia MUSIC TEST\n"]
    RESULT_LINES["fix_letter_followed_by_space_C"] = ["TEST Cynthia MUSIC TEST\n"]

    TEST_LINES["fix_italic_tag_errors_1"] = ["<i>Test </i>test<i> test </i>\n", "<i>Test</i>-<i>test</i>\n"]
    RESULT_LINES["fix_italic_tag_errors_1"] = ["<i>Test</i> test <i>test</i>\n", "<i>Test-test</i>\n"]
    TEST_LINES["fix_italic_tag_errors_2"] = ["<i>Test </i>Test<i>-</i>test\n", "<i> \" Test \" </i>\n"]
    RESULT_LINES["fix_italic_tag_errors_2"] = ["<i>Test</i> Test-test\n", "<i>\"Test\"</i>\n"]
    TEST_LINES["fix_italic_tag_errors_3"] = ["<i>Test</i> <i>Test</i> Test\n", "<i></i><i></i>Test<i></i>\n"]
    RESULT_LINES["fix_italic_tag_errors_3"] = ["<i>Test Test</i> Test\n", "Test\n"]

    TEST_LINES["fix_colon"] = ["TEST: line. Other test:\n", "12: 44 or 12 : 45 or 12 :45 or 12:46 or: 7\n"]
    RESULT_LINES["fix_colon"] = ["TEST : line. Other test :\n", "12:44 or 12:45 or 12:45 or 12:46 or : 7\n"]

    TEST_LINES["fix_common_misspells_:fr"] = ["Seinfelf. II. Evidemment\n"]
    RESULT_LINES["fix_common_misspells_:fr"] = ["Seinfeld. Il. Évidemment\n"]
    TEST_LINES["fix_common_misspells_:eng"] = ["Seinfelf. II yourjob\n"]
    RESULT_LINES["fix_common_misspells_:eng"] = ["Seinfeld. II your job\n"]
    TEST_LINES["fix_common_misspells"] = ["Seinfelf lran 9 mm\n"]
    RESULT_LINES["fix_common_misspells"] = ["Seinfeld Iran 9mm\n"]

    TEST_LINES["fix_numbers_:x"] = ["Line 333 4 45, 50\n", "4 ème et 5 h 30 à 20 % et 5 .\n"]
    RESULT_LINES["fix_numbers_:x"] = ["Line 333 445,50\n", "4ème et 5h30 à 20% et 5.\n"]
    TEST_LINES["fix_numbers_2"] = ["and 3, 4, 5\n", "4 ème et 5 h 30 à 20 % et 5 .\n"]
    RESULT_LINES["fix_numbers_2"] = ["and 3, 4, 5\n", "4ème et 5h30 à 20% et 5.\n"]

    TEST_LINES["fix_degree_symbol"] = ["n°1 and n° 2 and N ° 3 and n °4 and 5 °F and 6° F and 7 ° C\n"]
    RESULT_LINES["fix_degree_symbol"] = ["n°1 and n°2 and N°3 and n°4 and 5°F and 6°F and 7°C\n"]

    TEST_LINES["fix_capital_i_to_l"] = ["Il AIbert AI pIop, Iame Iame fataI AIIIIb\n"]
    RESULT_LINES["fix_capital_i_to_l"] = ["Il Albert AI plop, lame lame fatal Allllb\n"]

    TEST_LINES["fix_l_to_capital_i"] = ["lnter la test. ln MlB line\n", "Il lou lAB AllB ABll Xlll lll\n"]
    RESULT_LINES["fix_l_to_capital_i"] = ["Inter la test. In MIB line\n", "Il lou IAB AIIB ABII XIII III\n"]

    TEST_LINES["fix_acronyms"] = ["I. I was here. S. N. C. F. I was\n", "Line 2. I. Line 2. A.T. M. \n"]
    RESULT_LINES["fix_acronyms"] = ["I. I was here. S.N.C.F. I was\n", "Line 2. I. Line 2. A.T.M. \n"]


# noinspection SpellCheckingInspection
def populate_multi_line_test_dict():

    TEST_LINES["fix_redundant_italic_tag"] = ["<i>test</i> a <i>line 1</i>\n", "<i>test line 2</i>\n"]
    RESULT_LINES["fix_redundant_italic_tag"] = ["<i>test</i> a <i>line 1\n", "test line 2</i>\n"]

    TEST_LINES["fix_useless_dialog_hyphen_1"] = ["- test line\n"]
    RESULT_LINES["fix_useless_dialog_hyphen_1"] = ["test line\n"]
    TEST_LINES["fix_useless_dialog_hyphen_2"] = ["<i>- test line\n"]
    RESULT_LINES["fix_useless_dialog_hyphen_2"] = ["<i>test line\n"]
    TEST_LINES["fix_useless_dialog_hyphen_3"] = ["-  test line\n", "test line\n"]
    RESULT_LINES["fix_useless_dialog_hyphen_3"] = ["test line\n", "test line\n"]
    TEST_LINES["fix_useless_dialog_hyphen_4"] = ["<i>- test line\n", "test line\n"]
    RESULT_LINES["fix_useless_dialog_hyphen_4"] = ["<i>test line\n", "test line\n"]
    TEST_LINES["fix_useless_dialog_hyphen_5"] = ["\"- test line\n", "test\" line\n"]
    RESULT_LINES["fix_useless_dialog_hyphen_5"] = ["\"test line\n", "test\" line\n"]
    TEST_LINES["fix_useless_dialog_hyphen_6"] = ["\"<i>- test line\n", "test line\n", "test line\"\n"]
    RESULT_LINES["fix_useless_dialog_hyphen_6"] = ["\"<i>test line\n", "test line\n", "test line\"\n"]

    TEST_LINES["fix_missing_dialog_hyphen_1"] = ["<i>test line 1</i>\n", "- test line 2\n"]
    RESULT_LINES["fix_missing_dialog_hyphen_1"] = ["- <i>test line 1</i>\n", "- test line 2\n"]
    TEST_LINES["fix_missing_dialog_hyphen_2"] = ["<i>test line 1</i>\n", "- test line 2\n", "- test line 3\n"]
    RESULT_LINES["fix_missing_dialog_hyphen_2"] = ["- <i>test line 1</i>\n", "- test line 2\n", "- test line 3\n"]
    TEST_LINES["fix_missing_dialog_hyphen_3"] = ["<i>test line 1</i>\n", "test line 2\n", "- test line 3\n"]
    RESULT_LINES["fix_missing_dialog_hyphen_3"] = ["- <i>test line 1</i>\n", "test line 2\n", "- test line 3\n"]
    TEST_LINES["fix_missing_dialog_hyphen_4"] = [" - Aye, sir.\n", "- Incoming message, sir.\n"]
    RESULT_LINES["fix_missing_dialog_hyphen_4"] = [" - Aye, sir.\n", "- Incoming message, sir.\n"]

    TEST_LINES["fix_double_quotes_errors_1"] = ["test line 1\n", "test line\"\n"]
    RESULT_LINES["fix_double_quotes_errors_1"] = ["\"test line 1\n", "test line\"\n"]
    TEST_LINES["fix_double_quotes_errors_2"] = ["test \"line 1\n", "test\" line\n"]
    RESULT_LINES["fix_double_quotes_errors_2"] = ["test \"line 1\n", "test\" line\n"]
    TEST_LINES["fix_double_quotes_errors_3"] = ["<i>test line 1\n", "test line\"</i>\n"]
    RESULT_LINES["fix_double_quotes_errors_3"] = ["<i>\"test line 1\n", "test line\"</i>\n"]
    TEST_LINES["fix_double_quotes_errors_4"] = ["test \"line 1\n", "test line\"\n"]
    RESULT_LINES["fix_double_quotes_errors_4"] = ["test \"line 1\n", "test line\"\n"]
    TEST_LINES["fix_double_quotes_errors_5"] = ["- test line 1\n", "- test line\"\n"]
    RESULT_LINES["fix_double_quotes_errors_5"] = ["- test line 1\n", "- \"test line\"\n"]
    TEST_LINES["fix_double_quotes_errors_6"] = ["- <i>test line 1\"</i>\n", "- test line\n"]
    RESULT_LINES["fix_double_quotes_errors_6"] = ["- <i>\"test line 1\"</i>\n", "- test line\n"]

    TEST_LINES["fix_empty_lines_1"] = ["test line 1\n", "\n", "test line\n"]
    RESULT_LINES["fix_empty_lines_1"] = ["test line 1\n", "test line\n"]
    TEST_LINES["fix_empty_lines_2"] = ["test line 1\n", "  \n", "test line\n"]
    RESULT_LINES["fix_empty_lines_2"] = ["test line 1\n", "test line\n"]

    TEST_LINES["fix_sdh_tags_1"] = ["MAN ON RADIO : test line 1\n", "test line 2\n"]
    RESULT_LINES["fix_sdh_tags_1"] = ["test line 1\n", "test line 2\n"]
    TEST_LINES["fix_sdh_tags_2"] = ["- <i>MAN ON RADIO : test line 1\n", "- test line 2</i>\n"]
    RESULT_LINES["fix_sdh_tags_2"] = ["- <i>test line 1\n", "- test line 2</i>\n"]
    TEST_LINES["fix_sdh_tags_3"] = ["- <i>MAN 1 : test line 1</i>\n", "- test line 2\n"]
    RESULT_LINES["fix_sdh_tags_3"] = ["- <i>test line 1</i>\n", "- test line 2\n"]
    TEST_LINES["fix_sdh_tags_4"] = ["[PLOP]\n"]
    RESULT_LINES["fix_sdh_tags_4"] = ["\n"]
    TEST_LINES["fix_sdh_tags_5"] = ["[plop] truc\n"]
    RESULT_LINES["fix_sdh_tags_5"] = ["truc\n"]
    TEST_LINES["fix_sdh_tags_6"] = [" ? ploplop ? \n"]
    RESULT_LINES["fix_sdh_tags_6"] = ["\n"]
    TEST_LINES["fix_sdh_tags_7"] = ["tonight at 1:15.\n"]
    RESULT_LINES["fix_sdh_tags_7"] = ["tonight at 1:15.\n"]
    TEST_LINES["fix_sdh_tags_8"] = ["- (SHRIEKS) Oh.\n", "- (SCOFFS)\n", "<i>-(WHEE HERE) Test"]
    RESULT_LINES["fix_sdh_tags_8"] = ["- Oh.\n", "- \n", "<i>-Test"]

    TEST_LINES["fix_3d_doubles_1"] = ["A\n", "A\n"]
    RESULT_LINES["fix_3d_doubles_1"] = ["A\n"]
    TEST_LINES["fix_3d_doubles_2"] = ["A\n", "B\n", "C\n", "A\n", "B\n", "C\n"]
    RESULT_LINES["fix_3d_doubles_2"] = ["A\n", "B\n", "C\n"]
    TEST_LINES["fix_3d_doubles_3"] = ["A\n", "B\n", "C\n", "D\n", "A\n", "B\n", "C\n"]
    RESULT_LINES["fix_3d_doubles_3"] = ["A\n", "B\n", "C\n", "D\n", "A\n", "B\n", "C\n"]


populate_single_line_test_dict()
populate_multi_line_test_dict()


class TestStringsUtils(unittest.TestCase):

    # region Utils

    def test_remove_all_uppercase_words(self):

        line = ["TEST", "II", "Hey", "PLOP", "Moarf"]
        result = StringsUtils.remove_all_uppercase_words(line)

        self.assertEqual(result, ["II", "Hey", "Moarf"])

    # def test_print_single_letters(self):
    #
    #     lines = ["TEST\n", "II\n", "H", "J\nPLOP\n", "Test B.\n", "test n test\n"]
    #     results = [False, False, True, True, True, True]
    #
    #     for i in range(0, len(lines)):
    #         StringsUtils.print_single_letters(lines[i])
    #         output = sys.stdout.getvalue().strip()
    #         lines[i] = len(output) > 0
    #         print("== " + str(output))
    #
    #     print("lines   : " + str(lines))
    #     print("results : " + str(results))
    #     self.assertEqual(lines, results)

    # endregion Utils

    # region Single-line

    def test_fix_accentuated_capital_a(self):
        for key in TEST_LINES:
            corrected_line = []

            for i in range(0, len(TEST_LINES[key])):
                fake_input = ":x" if ":x" in key else ":q"
                with unittest.mock.patch('builtins.input', return_value=fake_input):
                    corrected_line.append(StringsUtils.fix_accentuated_capital_a(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_accentuated_capital_a")

    def test_fix_common_errors(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_common_errors(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_common_errors")

    def test_fix_punctuation_errors(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_punctuation_errors(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_punctuation_errors")

    def test_test_fix_quotes(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_quotes(TEST_LINES[key][i], "eng"))

            self.assert_list_equals(corrected_line, key, "fix_quotes")

    def test_fix_punctuation_spaces(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_punctuation_spaces(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_punctuation_spaces")

    def test_fix_dialog_hyphen(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_dialog_hyphen(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_dialog_hyphen")

    def test_fix_letter_followed_by_space(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                temp_lines = StringsUtils.fix_letter_followed_by_space(TEST_LINES[key][i], "f", "fr")
                temp_lines = StringsUtils.fix_letter_followed_by_space(temp_lines, "C", "eng")
                corrected_line.append(temp_lines)

            self.assert_list_equals(corrected_line, key, "fix_letter_followed_by_space")

    def test_fix_italic_tag_errors(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_italic_tag_errors(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_italic_tag_errors")

    def test_fix_colon(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_colon(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_colon")

    def test_fix_common_misspells(self):
        for key in TEST_LINES:
            corrected_line = []

            for i in range(0, len(TEST_LINES[key])):
                language = "eng" if ":eng" in key else "fr"
                corrected_line.append(StringsUtils.fix_common_misspells(TEST_LINES[key][i], language))

            self.assert_list_equals(corrected_line, key, "fix_common_misspells")

    def test_fix_numbers(self):
        for key in TEST_LINES:
            corrected_line = []

            for i in range(0, len(TEST_LINES[key])):
                fake_input = ":x" if ":x" in key else ":q"
                with unittest.mock.patch('builtins.input', return_value=fake_input):
                    corrected_line.append(StringsUtils.fix_numbers(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_numbers")

    def test_fix_degree_symbol(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_degree_symbol(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_degree_symbol")

    def test_fix_capital_i_to_I(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_capital_i_to_l(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_capital_i_to_l")

    def test_fix_l_to_capital_i(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_l_to_capital_i(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_l_to_capital_i")

    def test_fix_acronyms(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_acronyms(TEST_LINES[key][i]))

            self.assert_list_equals(corrected_line, key, "fix_acronyms")

    # endregion Single-line

    # region Multi-line

    def test_fix_3d_doubles(self):
        self.assertEqual(StringsUtils.fix_3d_doubles([]), [])
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_3d_doubles(TEST_LINES[key])
            self.assert_list_equals(corrected_lines, key, "fix_3d_doubles")

    def test_fix_empty_lines(self):
        self.assertEqual(StringsUtils.fix_empty_lines([]), [])
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_empty_lines(TEST_LINES[key])
            self.assert_list_equals(corrected_lines, key, "fix_empty_lines")

    def test_fix_redundant_italic_tag(self):
        self.assertEqual(StringsUtils.fix_redundant_italic_tag([]), [])
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_redundant_italic_tag(TEST_LINES[key])
            self.assert_list_equals(corrected_lines, key, "fix_redundant_italic_tag")

    def test_fix_useless_dialog_hyphen(self):
        self.assertEqual(StringsUtils.fix_useless_dialog_hyphen([]), [])
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_useless_dialog_hyphen(TEST_LINES[key])
            self.assert_list_equals(corrected_lines, key, "fix_useless_dialog_hyphen")

    def test_fix_missing_dialog_hyphen(self):
        self.assertEqual(StringsUtils.fix_missing_dialog_hyphen([]), [])
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_missing_dialog_hyphen(TEST_LINES[key])
            self.assert_list_equals(corrected_lines, key, "fix_missing_dialog_hyphen")

    def test_fix_double_quotes_errors(self):
        self.assertEqual(StringsUtils.fix_double_quotes_errors([]), [])
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_double_quotes_errors(TEST_LINES[key])
            self.assert_list_equals(corrected_lines, key, "fix_double_quotes_errors")

    def test_fix_sdh_tags(self):
        self.assertEqual(StringsUtils.fix_sdh_tags([]), [])
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_sdh_tags(TEST_LINES[key])
            self.assert_list_equals(corrected_lines, key, "fix_sdh_tags")

    # endregion Multi-line

    def test_multi_line_errors(self):

        # We have to cleanup dictionary tests cases, to check only relevant lines.
        # Those dictionaries will be restored at the end of this test.
        Consts.fix_sdh_tags = True
        Consts.fix_3d_doubles = True
        TEST_LINES.clear()
        RESULT_LINES.clear()
        populate_multi_line_test_dict()
        corrected_lines = {}

        for key in TEST_LINES:
            fake_input = ":x" if ":x" in key else ":q"

            with unittest.mock.patch('builtins.input', return_value=fake_input):
                corrected_lines[key] = StringsUtils.fix_multi_line_errors(TEST_LINES[key])

        for key in corrected_lines:
            self.assertEqual(corrected_lines[key], RESULT_LINES[key])

        TEST_LINES.clear()
        RESULT_LINES.clear()
        populate_single_line_test_dict()
        populate_multi_line_test_dict()

    def test_fix_single_line_errors(self):

        # We have to cleanup dictionary tests cases, to check only relevant lines.
        # Those dictionaries will be restored at the end of this test.
        TEST_LINES.clear()
        RESULT_LINES.clear()
        populate_single_line_test_dict()
        corrected_lines = {}

        for key in TEST_LINES:
            corrected_lines[key] = []

            for line_index in range(0, len(TEST_LINES[key])):

                language = "eng" if ":eng" in key else "fr"
                fake_input = ":x" if ":x" in key else ":q"

                with unittest.mock.patch('builtins.input', return_value=fake_input):
                    corrected_lines[key].append(StringsUtils.fix_single_line_errors(TEST_LINES[key][line_index], language))

        for key in corrected_lines:
            self.assertEqual(corrected_lines[key], RESULT_LINES[key])

        TEST_LINES.clear()
        RESULT_LINES.clear()
        populate_single_line_test_dict()
        populate_multi_line_test_dict()

    def assert_list_equals(self, corrected_lines, key, tag):
        if tag in key:
            self.assertListEqual(corrected_lines, RESULT_LINES[key])
        else:
            self.assertListEqual(corrected_lines, TEST_LINES[key])


if __name__ == '__main__':
    unittest.main()
