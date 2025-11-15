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

import hashlib               # get MD5 hash of a file
import shutil                # copy backup files
import fnmatch               # recursive research in folders
import os                    # system calls (open directories)
import io                    # file encoding
import re                    # regex
import chardet               # detect file encoding


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
    srt_file = open(path, 'w', encoding='utf-8')
    
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
        with io.open(temp_file_name, mode='w', encoding='utf-8') as target:
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

    if path.endswith("ger.srt") \
            or path.endswith("[ger].srt"):
        language = "ger"
    elif path.endswith("fre.srt") \
            or path.endswith("fr.srt") \
            or path.endswith("[fre].srt") \
            or path.endswith("[mis].srt"):
        language = "fr"
    elif path.endswith("en.srt") \
            or path.endswith("eng.srt") \
            or path.endswith("[eng].srt"):
        language = "eng"

    return language


def detect_file_encoding(file_path, sample_size=8192):
    """Detect the character encoding of a file.

    Uses the chardet library to analyze file content and determine its encoding.
    Reads a sample of the file to improve performance for large files.

    :param file_path: string, path to the file to analyze
    :param sample_size: int, number of bytes to read for analysis (default: 8192)
    :return: dict with 'encoding' (str), 'confidence' (float), and 'language' (str or None)
             Returns None if file cannot be read or encoding cannot be detected
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(sample_size)

        if not raw_data:
            return None

        result = chardet.detect(raw_data)
        return result

    except (IOError, OSError) as e:
        print(f"Error reading file '{file_path}': {e}")
        return None


def convert_to_utf8(file_path, in_place=True, backup=True):
    """Convert a file to UTF-8 encoding automatically.

    Detects the current encoding and converts the file to UTF-8.
    Can create a backup before conversion and either modify in-place or create a new file.

    :param file_path: string, path to the file to convert
    :param in_place: bool, if True modifies the file in-place, if False creates .utf8 copy
    :param backup: bool, if True creates a backup before in-place conversion
    :return: dict with 'success' (bool), 'original_encoding' (str), 'confidence' (float),
             'new_file' (str or None) or None if conversion failed
    """
    # Detect current encoding
    encoding_info = detect_file_encoding(file_path)

    if not encoding_info or not encoding_info.get('encoding'):
        print(f"Could not detect encoding for '{file_path}'")
        return None

    detected_encoding = encoding_info['encoding']
    confidence = encoding_info.get('confidence', 0)

    # If already UTF-8, no conversion needed
    if detected_encoding.lower() in ['utf-8', 'utf8', 'ascii']:
        print(f"File '{file_path}' is already in {detected_encoding}")
        return {
            'success': True,
            'original_encoding': detected_encoding,
            'confidence': confidence,
            'new_file': None
        }

    try:
        # Read file with detected encoding
        with io.open(file_path, mode='r', encoding=detected_encoding, errors='ignore') as source:
            content = source.read()

        # Determine output file path
        if in_place:
            if backup:
                backup_file(file_path)
            output_path = file_path
        else:
            # Create a new file with .utf8 extension
            base, ext = os.path.splitext(file_path)
            output_path = f"{base}.utf8{ext}"

        # Write as UTF-8
        with io.open(output_path, mode='w', encoding='utf-8') as target:
            target.write(content)

        print(f"Converted '{file_path}' from {detected_encoding} to UTF-8 (confidence: {confidence:.2%})")

        return {
            'success': True,
            'original_encoding': detected_encoding,
            'confidence': confidence,
            'new_file': output_path if not in_place else None
        }

    except (IOError, OSError, UnicodeDecodeError) as e:
        print(f"Error converting file '{file_path}': {e}")
        return None
