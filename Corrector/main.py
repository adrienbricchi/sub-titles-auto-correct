#!/usr/bin/python3
# -*-coding:utf8 -*

# sub-titles-auto-correct
# Copyright (C) 2014-2016
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

from tkinter import Menu, Listbox, END, Label, Tk           # GUI, needs python3-tk package on Linux
import locale                                               # get current system language
from tkinter.filedialog import LoadFileDialog
import datetime
from Corrector.Models.Subtitle import *
from Corrector.Utils.FileUtils import *
from Corrector.Utils.StringsUtils import *


def build_menus(root):
    main_menu = Menu(root, tearoff=0)
    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label=translate("Exit"), command=root.quit)
    main_menu.add_cascade(label=translate("File"), menu=file_menu)
    root.config(menu=main_menu)
    return


def build_main_panel(root, path):
    listbox = Listbox(root)
    listbox.pack()

    for item in get_all_files(path, -1):
        listbox.insert(END, os.path.basename(item))

    champ_label = Label(root, text="Loaded")
    champ_label.pack()
    return


def build_and_launch_interface():
    root = Tk()
    build_menus(root)
    build_main_panel(root, "C:/")
    root.mainloop()
    return


def open_files(root):
    LoadFileDialog.files_select_event(root, None)
    return


''' ================================================== '''


french = {"Exit": "Quitter",
          "File": "Fichier"}

if locale.getdefaultlocale('LANGUAGE')[0] == 'fr_FR':
    current_dictionary = french


def translate(string):
    translation = string
    if current_dictionary:
        if string in current_dictionary:
            translation = current_dictionary[string]
        else:
            print("missing translation for '" + string + "'")
    return translation


''' ================================================== '''


# debug_path = "C:/Users/Adrien/Desktop/Corrector/"
# build_and_launch_interface()

# for file in get_files_with_type(get_all_files("C:/", 0), "srt") :

# file = "C:/note.srt"
# backup_file(file)


start = datetime.datetime.now()
# 11-20

files = get_files_with_type(get_all_files(Consts.root_path, 0), "srt")
for file in files:
    clean_space_in_filename(file)

prompt = input("script ou word ? : ")

# TODO : met- ; vince; ; ARl/LORl ; *_) ; Ibs ; l'chaim ; crappy ' ; lower case acronyms ; multi line deaf

files = get_files_with_type(get_all_files(Consts.root_path, 0), "srt")
for file in files:
    # backup_file(file)
    lines = get_file_text(file, True)
    print(SHELL_COLOR_BOLD + file + " (" + str(len(lines)) + " lines)" + SHELL_COLOR_END)
    current_language = get_file_language(file)

    if prompt.startswith("scri"):

        try:
            subtitles = Subtitle.subtitles_from_lines(lines)
        #except ValueError as err:
        #     #vprint(shell_color_fail + "Parsing error : " + str(err) + shell_color_end)
        #     backup_file(file)
        #     utf8_to_ansi(get_bak_file_name(file), file)
        #     lines = get_file_text(file, True)
        #     subtitles = Subtitle.subtitles_from_lines(lines)

            for subtitle in subtitles:

                corrected_lines = fix_multi_line_errors(subtitle.lines)
                subtitle.set_lines(corrected_lines)

                if len(subtitle.get_lines()) > 2:
                    print("Wrong subtitle size : " + str(subtitle.get_lines()))

                corrected_lines = []
                for line in subtitle.get_lines():

                    line = fix_single_line_errors(line, current_language)

                    array = find_words_with_char(line, "I", current_language)
                    array = remove_all_uppercase_words(array)
                    line = ask_for_correction(line, array, "I_trusted.csv", current_language)

                    pretty_number = subtitle.get_number().replace("\n", "")
                    pretty_line = line.replace("\n", "")

                    if "£" in line:
                        print(SHELL_COLOR_FAIL + "Found £ at " + pretty_number + SHELL_COLOR_END + " : " + pretty_line)

                    corrected_lines.append(line)

                subtitle.set_lines(corrected_lines)

            # Save file

            new_lines = []

            for subtitle in subtitles:
                if len(subtitle.lines) == 1 and re.match(r"^\s*\n*$", subtitle.lines[0]):
                    print("Empty subtitle found")
                elif len(subtitle.lines) > 0:
                    new_lines += subtitle.to_lines()
                    new_lines.append("\n")

            write_file(file, new_lines)

        except ValueError as err:
            print(SHELL_COLOR_FAIL + "Parsing error : " + str(err) + SHELL_COLOR_END)

    elif prompt.startswith("wor"):
        launch_ms_word_spell_check(file, current_language)

end = datetime.datetime.now()
print(end - start)
