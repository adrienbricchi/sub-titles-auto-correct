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

from Corrector.Utils.StringsUtils import *


class Subtitle:
    """
    Mainly an array of strings, with a time code
    """

    # region Static methods

    @staticmethod
    def subtitles_from_lines(lines):
        subtitles = []
        index = 0

        while index < len(lines):
            if is_index(lines, index):

                found_number = lines[index]
                index += 1

                found_time_code = lines[index]
                index += 1

                found_lines = []
                while index < len(lines) and not is_index(lines, index):
                    if not re.match(r"^$", lines[index]):
                        found_lines.append(lines[index])
                    index += 1

                subtitles.append(Subtitle(found_number, found_time_code, found_lines))
            else:
                if "ÿþ" in lines[index]:
                    raise ValueError("Unsupported encoding")

                index += 1

        return subtitles

    # endregion Static methods

    def __init__(self, number, time_code, lines):
        self.number = number
        self.time_code = time_code
        self.lines = lines

    # region Setter/getter

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_time_code(self):
        return self.time_code

    def set_time_code(self, time_code):
        self.time_code = time_code

    def get_lines(self):
        return self.lines

    def set_lines(self, lines):
        self.lines = lines

    # endregion Setter/getter

    def to_lines(self):
        result = [self.number, self.time_code]
        result += self.lines
        return result

    def pretty_print(self):
        result = force_string_size(self.number.replace("\n", ""), 5)
        result += self.number.replace("\n", "") + " : "
        result += self.time_code.replace("\n", "") + " "

        pretty_printed_array = []
        for line in self.lines:
            pretty_printed_array.append(line.replace("\n", ""))

        result += str(pretty_printed_array)
        return result
