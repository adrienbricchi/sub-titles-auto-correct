import unittest
from Corrector.Utils import StringsUtils


TEST_LINES = []
RESULT_LINES = []

TEST_LINES.append("<i>fix_redundant_italic_tag</i> <i>line 1</i><i></i>\n")
TEST_LINES.append("<i>fix_redundant_italic_tag</i><i> line 2</i>\n")
RESULT_LINES.append("<i>fix_redundant_italic_tag line 1\n")
RESULT_LINES.append("fix_redundant_italic_tag line 2</i>\n")


class TestStringsUtils(unittest.TestCase):

    def test_fix_redundant_italic_tag(self):
        corrected_lines = StringsUtils.fix_redundant_italic_tag(TEST_LINES)
        for i in range(0, len(corrected_lines)):
            if "fix_redundant_italic_tag" in TEST_LINES[i]:
                self.assertEqual(corrected_lines[i], RESULT_LINES[i])
            else:
                self.assertEqual(corrected_lines[i], TEST_LINES[i])


if __name__ == '__main__':
    unittest.main()
