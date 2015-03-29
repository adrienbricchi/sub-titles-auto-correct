#!/usr/bin/python3
# -*-coding:utf8 -*


from tkinter import Menu, Listbox, END, Label, Tk           # GUI, needs python3-tk package on Linux
import locale                                               # get current system language
from tkinter.filedialog import LoadFileDialog
import datetime
import Corrector.Models.Subtitle
from Corrector.Models.Subtitle import Subtitle
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


french = {}
french["Exit"] = "Quitter" 
french["File"] = "Fichier" 


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
root_path = "C:/Users/Adrien/workspace/sub-titles-auto-correct/Tests/"
files = get_files_with_type(get_all_files(root_path, 0), "srt")

print("")

for file in files:
    # backup_file(file)
    lines = get_file_text(file, True)
    print(file + " (" + str(len(lines)) + " lines)")
    current_language = get_file_language(file)

    subtitles = Subtitle.subtitles_from_lines(lines)
    for subtitle in subtitles:

        corrected_lines = []
        for line in subtitle.lines:

            line = fix_triple_dots(line)
            line = fix_numbers(line)
            line = fix_common_errors(line)
            line = fix_capital_i_to_l(line)
            line = fix_l_to_capital_i(line)
            line = fix_acronyms(line)
            line = fix_common_misspells(line, current_language)
            line = fix_letter_followed_by_space(line, "f", current_language)
            line = fix_letter_followed_by_space(line, "W", current_language)
            line = fix_letter_followed_by_space(line, "C", current_language)
            line = fix_letter_followed_by_space(line, "G", current_language)
            line = fix_letter_followed_by_space(line, "Z", current_language)
            line = fix_letter_followed_by_space(line, "V", current_language)
            line = fix_quotes(line, current_language)
            line = fix_question_marks(line)
            line = fix_exclamation_marks(line)
            line = fix_dialog_hyphen(line)

            corrected_lines.append(line)

            pretty_number = subtitle.get_number().replace("\n", "")
            pretty_line = line.replace("\n", "")
            print_if_found_char(pretty_number, pretty_line, "°", current_language)
            print_if_found_char(pretty_number, pretty_line, "£", current_language)
            print_if_found_char(pretty_number, pretty_line, "I", current_language)

        subtitle.set_lines(corrected_lines)

    # Save file

    new_lines = []

    for subtitle in subtitles:
        new_lines += subtitle.to_lines()
        new_lines.append("\n")

    write_file(file, new_lines)

    # launch_ms_word_spell_check(file, file_language)

end = datetime.datetime.now()
print(end - start)
