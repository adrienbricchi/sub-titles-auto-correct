#!/usr/bin/python3
# -*-coding:utf8 -*

import hashlib               # get MD5 hash of a file
import shutil                # copy backup files
import fnmatch               # recursive research in folders
import os                    # system calls (open directories)


def get_file_text(path, mode_lines):
    """Opens a file and return the full string in it.

    :param path: string, the root path.
    :param mode_lines: bool, mode lines or not
    :return: string
    """
    srt_file = open(path, 'r', encoding='cp1252')
    
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
    srt_file = open(path, 'w', encoding='cp1252')
    
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
