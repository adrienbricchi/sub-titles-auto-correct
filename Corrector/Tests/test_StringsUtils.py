#!/usr/bin/python3
# -*-coding:utf8 -*

import unittest
from Corrector.Utils import StringsUtils
from Corrector.Utils import Consts


Consts.is_unittest_exec = True
TEST_LINES = {}
RESULT_LINES = {}

# region TEST_LINES Single

TEST_LINES["fix_numbers"] = ["Line 333 4 45, 50 and 3, 4, 5\n", "4 ème et 5 h 30 à 20 % et 5 .\n"]
RESULT_LINES["fix_numbers"] = ["Line 333 445,50 and 3, 4, 5\n", "4ème et 5h30 à 20% et 5.\n"]

TEST_LINES["fix_acronyms"] = ["I. I was here. S. N. C. F. I was\n", "Line 2. I. Line 2. A.T. M. \n"]
RESULT_LINES["fix_acronyms"] = ["I. I was here. S.N.C.F. I was\n", "Line 2. I. Line 2. A.T.M. \n"]

TEST_LINES["fix_punctuation_spaces"] = ["Hey! ?What ? ! ? !!\n", "Ok ! \"Line 2?\"?\n"]
RESULT_LINES["fix_punctuation_spaces"] = ["Hey !? What ?!?!!\n", "Ok ! \"Line 2 ?\" ?\n"]

# endregion TEST_LINES Single

# region TEST_LINES Multi

TEST_LINES["fix_redundant_italic_tag"] = ["<i>test</i> <i>line 1</i><i></i>\n", "<i>test</i><i> line 2</i>\n"]
RESULT_LINES["fix_redundant_italic_tag"] = ["<i>test line 1\n", "test line 2</i>\n"]

TEST_LINES["fix_useless_dialog_hyphen_1"] = ["- test line\n"]
RESULT_LINES["fix_useless_dialog_hyphen_1"] = ["test line\n"]
TEST_LINES["fix_useless_dialog_hyphen_2"] = ["<i>- test line\n"]
RESULT_LINES["fix_useless_dialog_hyphen_2"] = ["<i>test line\n"]
TEST_LINES["fix_useless_dialog_hyphen_3"] = ["-  test line\n", "test line\n"]
RESULT_LINES["fix_useless_dialog_hyphen_3"] = ["test line\n", "test line\n"]
TEST_LINES["fix_useless_dialog_hyphen_4"] = ["<i>- test line\n", "test line\n"]
RESULT_LINES["fix_useless_dialog_hyphen_4"] = ["<i>test line\n", "test line\n"]
TEST_LINES["fix_useless_dialog_hyphen_5"] = ["\"- test line\n", "test line\n"]
RESULT_LINES["fix_useless_dialog_hyphen_5"] = ["\"test line\n", "test line\n"]
TEST_LINES["fix_useless_dialog_hyphen_6"] = ["\"<i>- test line\n", "test line\n", "test line\n"]
RESULT_LINES["fix_useless_dialog_hyphen_6"] = ["\"<i>test line\n", "test line\n", "test line\n"]

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


# endregion TEST_LINES Multi


class TestStringsUtils(unittest.TestCase):

    # region Utils

    def assert_list_equals_test(self, corrected_lines, key, tag):
        if tag in key:
            self.assertListEqual(corrected_lines, RESULT_LINES[key])
        else:
            self.assertListEqual(corrected_lines, TEST_LINES[key])

    # endregion Utils

    # region Single-line

    def test_fix_numbers(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_numbers(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_numbers")

    def test_fix_punctuation_spaces(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_punctuation_spaces(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_punctuation_spaces")

    def test_fix_acronyms(self):
        for key in TEST_LINES:
            corrected_line = []
            for i in range(0, len(TEST_LINES[key])):
                corrected_line.append(StringsUtils.fix_acronyms(TEST_LINES[key][i]))

            self.assert_list_equals_test(corrected_line, key, "fix_acronyms")

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


if __name__ == '__main__':
    unittest.main()
