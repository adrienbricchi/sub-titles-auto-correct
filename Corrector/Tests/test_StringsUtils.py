import unittest
from Corrector.Utils import StringsUtils


TEST_LINES = {}
RESULT_LINES = {}

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


class TestStringsUtils(unittest.TestCase):

    def test_fix_redundant_italic_tag(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_redundant_italic_tag(TEST_LINES[key])
            if "fix_redundant_italic_tag" in key:
                self.assertListEqual(corrected_lines, RESULT_LINES[key])
            else:
                self.assertListEqual(corrected_lines, TEST_LINES[key])

    def test_fix_useless_dialog_hyphen(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_useless_dialog_hyphen(TEST_LINES[key])
            if "fix_useless_dialog_hyphen" in key:
                self.assertListEqual(corrected_lines, RESULT_LINES[key])
            else:
                self.assertListEqual(corrected_lines, TEST_LINES[key])

    def test_fix_missing_dialog_hyphen(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_missing_dialog_hyphen(TEST_LINES[key])
            if "fix_missing_dialog_hyphen" in key:
                self.assertListEqual(corrected_lines, RESULT_LINES[key])
            else:
                self.assertListEqual(corrected_lines, TEST_LINES[key])

    def test_fix_double_quotes_errors(self):
        for key in TEST_LINES:
            corrected_lines = StringsUtils.fix_double_quotes_errors(TEST_LINES[key])
            if "fix_double_quotes_errors" in key:
                self.assertListEqual(corrected_lines, RESULT_LINES[key])
            else:
                self.assertListEqual(corrected_lines, TEST_LINES[key])


if __name__ == '__main__':
    unittest.main()
