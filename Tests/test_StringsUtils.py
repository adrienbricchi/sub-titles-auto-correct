#!/usr/bin/python3
# -*-coding:utf8 -*

# sub-titles-auto-correct
# Copyright (C) 2014-2017
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
from Corrector.Utils import StringsUtils
from Corrector.Utils import Consts


Consts.is_unittest_exec = True

TEST_LINES = {}
RESULT_LINES = {}
RESULT_PROMPT = {}


# noinspection SpellCheckingInspection
def populate_single_line_test_dict():

    TEST_LINES["fix_punctuation_spaces"] = ["Hey! ?What ? ! ? !!\n", "Ok ! \"Line 2?\"?\n"]
    RESULT_LINES["fix_punctuation_spaces"] = ["Hey !? What ?!?!!\n", "Ok ! \"Line 2 ?\" ?\n"]

    TEST_LINES["fix_dialog_hyphen_1"] = ["-Plop\n", "--Plop\n", "-\"Plop\n"]
    RESULT_LINES["fix_dialog_hyphen_1"] = ["- Plop\n", "--Plop\n", "- \"Plop\n"]
    TEST_LINES["fix_dialog_hyphen_2"] = ["<i>-Plop\n", "\"-Plop\n", "\"-... Plop\n"]
    RESULT_LINES["fix_dialog_hyphen_2"] = ["<i>- Plop\n", "\"- Plop\n", "\"- ... Plop\n"]

    TEST_LINES["fix_italic_tag_errors_1"] = ["<i>Test </i>test<i> test </i>\n", "<i>Test</i>-<i>test</i>\n"]
    RESULT_LINES["fix_italic_tag_errors_1"] = ["<i>Test</i> test <i>test</i>\n", "<i>Test-test</i>\n"]
    TEST_LINES["fix_italic_tag_errors_2"] = ["<i>Test </i>Test<i>-</i>test\n", "<i> \" Test \" </i>\n"]
    RESULT_LINES["fix_italic_tag_errors_2"] = ["<i>Test</i> Test-test\n", "<i>\"Test\"</i>\n"]
    TEST_LINES["fix_italic_tag_errors_3"] = ["<i>Test</i> <i>Test</i> Test\n", "<i></i><i></i>Test<i></i>\n"]
    RESULT_LINES["fix_italic_tag_errors_3"] = ["<i>Test Test</i> Test\n", "Test\n"]

    TEST_LINES["fix_colon"] = ["TEST: line. Other test:\n", "12: 44 or 12 : 45 or 12 :45 or 12:46 or: 7\n"]
    RESULT_LINES["fix_colon"] = ["TEST : line. Other test :\n", "12:44 or 12:45 or 12:45 or 12:46 or : 7\n"]

    TEST_LINES["fix_common_misspells_fr"] = ["Seinfelf. II. Evidemment\n"]
    RESULT_LINES["fix_common_misspells_fr"] = ["Seinfeld. Il. Évidemment\n"]
    TEST_LINES["fix_common_misspells_eng"] = ["Seinfelf. II yourjob\n"]
    RESULT_LINES["fix_common_misspells_eng"] = ["Seinfeld. II your job\n"]
    TEST_LINES["fix_common_misspells"] = ["Seinfelf lran 9 mm\n"]
    RESULT_LINES["fix_common_misspells"] = ["Seinfeld Iran 9mm\n"]

    TEST_LINES["fix_numbers_1"] = ["Line 333 4 45, 50\n", "4 ème et 5 h 30 à 20 % et 5 .\n"]
    RESULT_LINES["fix_numbers_1"] = ["Line 333 445,50\n", "4ème et 5h30 à 20% et 5.\n"]
    TEST_LINES["fix_numbers_2"] = ["and 3, 4, 5\n", "4 ème et 5 h 30 à 20 % et 5 .\n"]
    RESULT_LINES["fix_numbers_2"] = ["and 3, 4, 5\n", "4ème et 5h30 à 20% et 5.\n"]

    TEST_LINES["fix_degree_symbol"] = ["n°1 and n° 2 and N ° 3 and n °4 and 5 °F and 6° F and 7 ° C\n"]
    RESULT_LINES["fix_degree_symbol"] = ["n°1 and n°2 and N°3 and n°4 and 5°F and 6°F and 7°C\n"]

    TEST_LINES["fix_capital_i_to_l"] = ["Il AIbert AI pIop fataI AIIIIb\n"]
    RESULT_LINES["fix_capital_i_to_l"] = ["Il Albert AI plop fatal Allllb\n"]

    TEST_LINES["fix_l_to_capital_i"] = ["lnter la test. ln MlB line\n", "Il lou AllB ABll Xlll lll\n"]
    RESULT_LINES["fix_l_to_capital_i"] = ["Inter la test. In MIB line\n", "Il lou AIIB ABII XIII III\n"]

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
    TEST_LINES["fix_sdh_tags_2"] = ["- <i>MAN ON RADIO : test line 1\n", "test line 2</i>\n"]
    RESULT_LINES["fix_sdh_tags_2"] = ["- <i>test line 1\n", "test line 2</i>\n"]
    TEST_LINES["fix_sdh_tags_3"] = ["<i>MAN 1 : test line 1</i>\n", "- test line 2\n"]
    RESULT_LINES["fix_sdh_tags_3"] = ["- <i>test line 1</i>\n", "- test line 2\n"]
    TEST_LINES["fix_sdh_tags_4"] = ["[PLOP]\n"]
    RESULT_LINES["fix_sdh_tags_4"] = [""]


populate_single_line_test_dict()
populate_multi_line_test_dict()


class TestStringsUtils(unittest.TestCase):

    # region Single-line

    # TODO : test_fix_accentuated_capital_a
    # TODO : test_fix_common_errors
    # TODO : test_fix_punctuation_errors
    # TODO : test_fix_quotes

    def test_fix_punctuation_spaces(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_punctuation_spaces(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_punctuation_spaces")

    def test_fix_dialog_hyphen(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_dialog_hyphen(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_dialog_hyphen")

    # TODO : test_fix_letter_followed_by_space

    def test_fix_italic_tag_errors(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_italic_tag_errors(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_italic_tag_errors")

    def test_fix_colon(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_colon(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_colon")

    def test_fix_common_misspells(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                if "eng" in key:
                    corrected_line.append(StringsUtils.fix_common_misspells(TEST_LINES[key][i], "eng"))
                else:
                    corrected_line.append(StringsUtils.fix_common_misspells(TEST_LINES[key][i], "fr"))

            self.assert_list_equals_test(corrected_line, key, "fix_common_misspells")

    def test_fix_numbers(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                if "fix_numbers_1" in key:
                    with unittest.mock.patch('builtins.input', return_value=':x'):
                        corrected_line.append(StringsUtils.fix_numbers(TEST_LINES[key][i]))
                elif "fix_numbers_2" in key:
                    with unittest.mock.patch('builtins.input', return_value=':q'):
                        corrected_line.append(StringsUtils.fix_numbers(TEST_LINES[key][i]))
                else:
                    corrected_line.append(StringsUtils.fix_numbers(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_numbers")

    def test_fix_degree_symbol(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_degree_symbol(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_degree_symbol")

    def test_fix_capital_i_to_I(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_capital_i_to_l(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_capital_i_to_l")

    def test_fix_l_to_capital_i(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_l_to_capital_i(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_l_to_capital_i")

    def test_fix_acronyms(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_acronyms(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_acronyms")

    # endregion Single-line

    # region Multi-line

    def test_fix_empty_lines(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_empty_lines(TEST_LINES[key])
            self.assert_list_equals_test(corrected_lines, key, "fix_empty_lines")

    def test_fix_redundant_italic_tag(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_redundant_italic_tag(TEST_LINES[key])
            self.assert_list_equals_test(corrected_lines, key, "fix_redundant_italic_tag")

    def test_fix_useless_dialog_hyphen(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_useless_dialog_hyphen(TEST_LINES[key])
            self.assert_list_equals_test(corrected_lines, key, "fix_useless_dialog_hyphen")

    def test_fix_missing_dialog_hyphen(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_missing_dialog_hyphen(TEST_LINES[key])
            self.assert_list_equals_test(corrected_lines, key, "fix_missing_dialog_hyphen")

    def test_fix_double_quotes_errors(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_double_quotes_errors(TEST_LINES[key])
            self.assert_list_equals_test(corrected_lines, key, "fix_double_quotes_errors")

    def test_fix_sdh_tags(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_sdh_tags(TEST_LINES[key])
            self.assert_list_equals_test(corrected_lines, key, "fix_sdh_tags")

    # endregion Multi-line

    def assert_list_equals_test(self, corrected_lines, key, tag):
        if tag in key:
            self.assertListEqual(corrected_lines, RESULT_LINES[key])
        else:
            self.assertListEqual(corrected_lines, TEST_LINES[key])


if __name__ == '__main__':
    unittest.main()
