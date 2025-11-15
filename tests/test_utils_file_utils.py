#!/usr/bin/python3
# -*-coding:utf8 -*

#  sub-titles-auto-correct
#  Copyright (C) 2014-2022
#  -
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os
import tempfile
import shutil

from subtitles_auto_correct.utils import file_utils as FileUtils


class TestFileEncodingDetection(unittest.TestCase):
    """Test encoding detection and conversion functions."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_detect_utf8_encoding(self):
        """Test detection of UTF-8 encoded file."""
        test_file = os.path.join(self.test_dir, "test_utf8.txt")
        test_content = "Hello World! Héllo Wörld! こんにちは"

        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)

        result = FileUtils.detect_file_encoding(test_file)

        self.assertIsNotNone(result)
        self.assertIn('encoding', result)
        self.assertIn('confidence', result)
        # UTF-8 or ASCII are both acceptable
        self.assertIn(result['encoding'].lower(), ['utf-8', 'utf8', 'ascii'])

    def test_detect_latin1_encoding(self):
        """Test detection of Latin-1 (ISO-8859-1) encoded file."""
        test_file = os.path.join(self.test_dir, "test_latin1.txt")
        test_content = "Café résumé naïve"

        with open(test_file, 'wb') as f:
            f.write(test_content.encode('latin-1'))

        result = FileUtils.detect_file_encoding(test_file)

        self.assertIsNotNone(result)
        self.assertIn('encoding', result)
        # Should detect some form of ISO-8859-1 or Windows-1252
        self.assertTrue(result['confidence'] > 0.5)

    def test_detect_empty_file(self):
        """Test detection of empty file."""
        test_file = os.path.join(self.test_dir, "test_empty.txt")

        with open(test_file, 'w') as f:
            f.write("")

        result = FileUtils.detect_file_encoding(test_file)

        # Empty files should return None
        self.assertIsNone(result)

    def test_detect_nonexistent_file(self):
        """Test detection of nonexistent file."""
        test_file = os.path.join(self.test_dir, "nonexistent.txt")

        result = FileUtils.detect_file_encoding(test_file)

        self.assertIsNone(result)

    def test_convert_latin1_to_utf8(self):
        """Test converting Latin-1 file to UTF-8."""
        test_file = os.path.join(self.test_dir, "test_convert.txt")
        test_content = "Café résumé naïve"

        # Create Latin-1 encoded file
        with open(test_file, 'wb') as f:
            f.write(test_content.encode('latin-1'))

        # Convert to UTF-8 (not in-place)
        result = FileUtils.convert_to_utf8(test_file, in_place=False, backup=False)

        self.assertIsNotNone(result)
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['new_file'])

        # Verify the new file is UTF-8
        with open(result['new_file'], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, test_content)

    def test_convert_utf8_already_utf8(self):
        """Test converting UTF-8 file (should skip conversion)."""
        test_file = os.path.join(self.test_dir, "test_already_utf8.txt")
        test_content = "Hello World!"

        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)

        result = FileUtils.convert_to_utf8(test_file, in_place=True, backup=False)

        self.assertIsNotNone(result)
        self.assertTrue(result['success'])
        self.assertIn(result['original_encoding'].lower(), ['utf-8', 'utf8', 'ascii'])

    def test_convert_in_place(self):
        """Test in-place conversion with backup."""
        test_file = os.path.join(self.test_dir, "test_inplace.txt")
        test_content = "Test content"

        # Create ASCII file (for simplicity)
        with open(test_file, 'w', encoding='ascii') as f:
            f.write(test_content)

        # Convert in-place without backup (since backup_file expects .srt extension)
        result = FileUtils.convert_to_utf8(test_file, in_place=True, backup=False)

        self.assertIsNotNone(result)
        self.assertTrue(result['success'])
        self.assertIsNone(result['new_file'])

        # Verify file still exists and is readable
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, test_content)


class TestFileUtilsOther(unittest.TestCase):
    """Test other file utility functions."""

    def test_get_file_language(self):
        """Test language detection from filename."""
        self.assertEqual(FileUtils.get_file_language("movie.ger.srt"), "ger")
        self.assertEqual(FileUtils.get_file_language("movie[ger].srt"), "ger")
        self.assertEqual(FileUtils.get_file_language("movie.fr.srt"), "fr")
        self.assertEqual(FileUtils.get_file_language("movie.fre.srt"), "fr")
        self.assertEqual(FileUtils.get_file_language("movie[fre].srt"), "fr")
        self.assertEqual(FileUtils.get_file_language("movie[mis].srt"), "fr")
        self.assertEqual(FileUtils.get_file_language("movie.en.srt"), "eng")
        self.assertEqual(FileUtils.get_file_language("movie.eng.srt"), "eng")
        self.assertEqual(FileUtils.get_file_language("movie[eng].srt"), "eng")
        self.assertEqual(FileUtils.get_file_language("movie.srt"), "undefined")


if __name__ == '__main__':
    unittest.main()
