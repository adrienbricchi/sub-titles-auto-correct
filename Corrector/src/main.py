#!/usr/bin/python3
# -*-coding:utf8 -*


from tkinter import Menu, Listbox, END, Label, Tk           # GUI, needs python3-tk package on Linux
import locale                                               # get current system language
from tkinter.filedialog import LoadFileDialog
import datetime
import sys
import re
from FileUtils import *
from StringsUtils import *


''' ================================================== '''


def build_menus(root) :
    main_menu = Menu(root, tearoff=0)
    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label=translate("Exit"), command=root.quit)
    main_menu.add_cascade(label=translate("File"), menu=file_menu)
    root.config(menu = main_menu)
    return


def build_main_panel(root, path) :
    listbox = Listbox(root)
    listbox.pack()
    for item in get_all_files(path) :
        listbox.insert(END, os.path.basename(item))
    champ_label = Label(root, text="Loaded")
    champ_label.pack()
    return


def build_and_launch_interface() :
    root = Tk()
    build_menus(root)
    build_main_panel(root, "C:/")
    root.mainloop()
    return


def open_files(root) :
    LoadFileDialog.files_select_event(root, None)
    return


''' ================================================== '''


french = {}
french["Exit"] = "Quitter" 
french["File"] = "Fichier" 

if (locale.getdefaultlocale('LANGUAGE')[0] == 'fr_FR') :
    current_dictionnary = french


def translate(string) :
    translation = string
    if (current_dictionnary != None) :
        if (string in current_dictionnary) :
            translation = current_dictionnary[string]
        else :
            print("missing translation for '" + string + "'")
    return translation


''' ================================================== '''


#debug_path = "C:/Users/Adrien/Desktop/Corrector/"
#build_and_launch_interface()

#for file in get_files_with_type(get_all_files("C:/", 0), "srt") :

#file = "C:/note.srt"
#backup_file(file)

start = datetime.datetime.now()
#11-20
rootpath = "C:/Users/Adrien/Desktop/Seinfeld 7/"
files = get_files_with_type(get_all_files(rootpath, 3), "srt")

print("")

for file in files :
    if file.endswith("note.srt") or file.endswith("notes.srt") :
        lines = get_file_text(file, True)
        print("\n" + file)
        new_lines = []
        for line in lines :
            line = fix_triple_dots(line)
            line = fix_recurent_mispells(line)
            line = fix_letter_followed_by_space(line, "f")
            line = fix_letter_followed_by_space(line, "W")
            line = fix_letter_followed_by_space(line, "C")
            line = fix_letter_followed_by_space(line, "G")
            line = fix_letter_followed_by_space(line, "Z")
            line = fix_letter_followed_by_space(line, "V")
            line = fix_quotes(line)
            new_lines.append(line)
            
end = datetime.datetime.now()
print(end - start)

#print(new_lines)
#write_file(file, new_lines)