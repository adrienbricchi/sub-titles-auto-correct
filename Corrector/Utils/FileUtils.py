#!/usr/bin/python3
# -*-coding:utf8 -*

# sub-titles-auto-correct
# Copyright (C) 2014-2018
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

import hashlib               # get MD5 hash of a file
import shutil                # copy backup files
import fnmatch               # recursive research in folders
import os                    # system calls (open directories)
import io                    # file encoding
import re                    # regex


def clean_space_in_filename(file_path):
    """Rename a file replacing spaces with underscore.

    :param file_path: string
    """
    new_path = re.sub(r"(\s)(?=[^/]*$)", r"_", file_path)
    os.rename(file_path, new_path)


def get_file_text(path, mode_lines):
    """Opens a file and return the full string in it.

    :param path: string, the root path.
    :param mode_lines: bool, mode lines or not
    :return: string
    """
    srt_file = open(path, 'r', encoding='utf-8-sig')
    
    if mode_lines:
        srt_content = srt_file.readlines()
    else:
        srt_content = srt_file.read()

    srt_file.close()
    return srt_content


def get_bak_file_name(path):
    """Return file path with suffix.

    :param path: string, the root path.
    :return: string
    """
    return path[:-4] + " (before STAC)" + path[-4:]


def get_files_with_type(file_list, file_type):
    """Return files with the given type (except backups).

    :param file_list: list of string, files path list to filter.
    :param file_type: string, the file_type suffix
    :return: list of string
    """
    srt_list = []
    
    for file in fnmatch.filter(file_list, '*.' + file_type):
        srt_list.append(file)

    srt_list = [file for file in srt_list if (file[-17:-4] != "(before STAC)")]
    srt_list = [file for file in srt_list if (file[-20:-4] != "(Avant SRAH 2.3)")]
    return srt_list


def get_all_files(root, depth):
    """Return all files in the given path

    :param root: string, the root path.
    :param depth: int, the recursive depth.
    :return: list of string
    """
    file_list = []
    
    for item in os.listdir(root):
        if os.path.isfile(os.path.join(root, item)):
            file_list.append(os.path.join(root, item))
        elif os.path.isdir(os.path.join(root, item)):
            if (depth > 0) and (isinstance(item, str)):
                sub_depth = depth - 1
                try:
                    file_list += get_all_files(os.path.join(root, item), int(sub_depth))
                except PermissionError:
                    print("Warning : can't open '" + item + "' directory, permission denied")

    return file_list


def backup_file(path):
    """Creates a copy of the given file, if his backup file doesn't already exists

    :param path: string: the root path.
    :return:
    """
    if not os.path.isfile(get_bak_file_name(path)):
        shutil.copy(path, get_bak_file_name(path))
        
    return


def write_file(path, lines):
    """Save file

    :param path: string, the target file path.
    :param lines: list of string, file content
    :return:
    """
    srt_file = open(path, 'w', encoding='utf-8-sig')
    
    for line in lines:
        srt_file.write(line)
        
    srt_file.close()
    return


def get_md5(file):
    """Get the MD5 hash of a file
    
    :param: string, the target file path.
    :return: string
    """
    md5 = hashlib.md5()
    
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''): 
            md5.update(chunk)
            
    return md5.digest()


def ansi_to_utf8(source_path):
    """Changes data encoding.

    :param: string, the source file path.
    :param: string, the target file path.
    """
    temp_file_name = source_path + "_utf8.temp"

    with io.open(source_path, encoding='cp1252', errors='ignore') as source:
        with io.open(temp_file_name, mode='w', encoding='utf-8-sig') as target:
            shutil.copyfileobj(source, target)

    os.remove(source_path)
    os.rename(temp_file_name, source_path)

    return


def get_file_language(path):
    """Defines subtitle language, from suffix file name.

    :param path: file path
    :return:
    """
    language = "undefined"

    if path.endswith("fre.srt") or path.endswith("fr.srt") or path.endswith("[fre].srt") or path.endswith("[mis].srt"):
        language = "fr"
    elif path.endswith("en.srt") or path.endswith("eng.srt") or path.endswith("[eng].srt"):
        language = "eng"

    return language
