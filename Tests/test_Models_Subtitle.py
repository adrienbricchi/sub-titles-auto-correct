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
from Corrector.Models.Subtitle import *


SRT_SUBTITLES = ["1\n",
                 "00:02:17,440 --> 00:02:20,375\n",
                 "Test 1 line 1.\n",
                 "Test 1 line 2.\n",
                 "\n",
                 "2\n",
                 "00:02:20,476 --> 00:02:22,501\n",
                 "Test 2 line 1.\n",
                 "\n",
                 "2\n",
                 "00:02:23,741 --> 00:02:25,651\n",
                 "Test 3 line 1.\n",
                 "2.\n",
                 "Test 3 line 3.\n",
                 "\n"]

SRT_SUBTITLES_PRETTY_PRINT = ["1    1 : 00:02:17,440 --> 00:02:20,375 ['Test 1 line 1.', 'Test 1 line 2.']",
                              "2    2 : 00:02:20,476 --> 00:02:22,501 ['Test 2 line 1.']",
                              "2    2 : 00:02:23,741 --> 00:02:25,651 ['Test 3 line 1.', '2.', 'Test 3 line 3.']"]

NOT_SRT_SUBTITLE = ["[Events]\n"
                    "Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text,\n",
                    "Dialogue: Marked=0,0:02:40.65,0:02:41.79,Wolf main,Cher,0000,0000,0000,,Line 1\n",
                    "Dialogue: Marked=0,0:02:42.42,0:02:44.15,Wolf main,autre,0000,0000,0000,,Line 2\n"]

BAD_ENCODING_SUBTITLE = ["ÿþ\n"]


class TestSubtitle(unittest.TestCase):

    def test_is_index(self):
        self.assertTrue(Subtitle.is_index(SRT_SUBTITLES, 0))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 1))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 2))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 3))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 4))
        self.assertTrue(Subtitle.is_index(SRT_SUBTITLES, 5))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 6))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 7))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 8))
        self.assertTrue(Subtitle.is_index(SRT_SUBTITLES, 9))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 10))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 11))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 12))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 13))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 14))
        self.assertFalse(Subtitle.is_index(None, 100))
        self.assertFalse(Subtitle.is_index(SRT_SUBTITLES, 100))

    def test_is_time_code(self):
        self.assertFalse(None)
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[0]))
        self.assertTrue(Subtitle.is_time_code(SRT_SUBTITLES[1]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[2]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[3]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[4]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[5]))
        self.assertTrue(Subtitle.is_time_code(SRT_SUBTITLES[6]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[7]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[8]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[9]))
        self.assertTrue(Subtitle.is_time_code(SRT_SUBTITLES[10]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[11]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[12]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[13]))
        self.assertFalse(Subtitle.is_time_code(SRT_SUBTITLES[14]))

    def test_is_text_line(self):
        self.assertFalse(Subtitle.is_text_line(SRT_SUBTITLES, 0))
        self.assertFalse(Subtitle.is_text_line(SRT_SUBTITLES, 1))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 2))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 3))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 4))
        self.assertFalse(Subtitle.is_text_line(SRT_SUBTITLES, 5))
        self.assertFalse(Subtitle.is_text_line(SRT_SUBTITLES, 6))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 7))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 8))
        self.assertFalse(Subtitle.is_text_line(SRT_SUBTITLES, 9))
        self.assertFalse(Subtitle.is_text_line(SRT_SUBTITLES, 10))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 11))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 12))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 13))
        self.assertTrue(Subtitle.is_text_line(SRT_SUBTITLES, 14))
        self.assertFalse(Subtitle.is_text_line(None, 100))
        self.assertFalse(Subtitle.is_text_line(SRT_SUBTITLES, 100))

    def test_subtitles_from_lines(self):
        srt_parsed = Subtitle.subtitles_from_lines(SRT_SUBTITLES)
        not_srt_parsed = Subtitle.subtitles_from_lines(NOT_SRT_SUBTITLE)
        self.assertEquals(len(srt_parsed), 3)
        self.assertEquals(len(not_srt_parsed), 0)
        with self.assertRaises(ValueError):
            Subtitle.subtitles_from_lines(BAD_ENCODING_SUBTITLE)

    def test_setters_getters(self):
        srt_parsed = Subtitle.subtitles_from_lines(SRT_SUBTITLES)
        srt_subtitle_0 = Subtitle(None, None, None)
        srt_subtitle_0.set_number("1\n")
        srt_subtitle_0.set_time_code("00:02:17,440 --> 00:02:20,375\n")
        srt_subtitle_0.set_lines(["Test 1 line 1.\n", "Test 1 line 2.\n"])
        self.assertEquals(srt_parsed[0].get_number(), srt_subtitle_0.get_number())
        self.assertEquals(srt_parsed[0].get_time_code(), srt_subtitle_0.get_time_code())
        self.assertEquals(srt_parsed[0].get_lines(), srt_subtitle_0.get_lines())

    def test_to_lines(self):
        srt_parsed = Subtitle.subtitles_from_lines(SRT_SUBTITLES)
        printed_lines = []
        for i in range(0, len(srt_parsed)):
            printed_lines += (srt_parsed[i].to_lines())
            printed_lines += "\n"
        self.assertEquals(printed_lines, SRT_SUBTITLES)

    def test_pretty_print(self):
        srt_parsed = Subtitle.subtitles_from_lines(SRT_SUBTITLES)
        for i in range(0, len(srt_parsed)):
            self.assertEquals(srt_parsed[i].pretty_print(), SRT_SUBTITLES_PRETTY_PRINT[i])


if __name__ == '__main__':
    unittest.main()
