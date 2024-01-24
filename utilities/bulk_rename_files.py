"""
File: bulk_rename_files.py
Author: Raphael Leveque
Date: November , 2023
Description: Recursively renames files in subdirectories by replacing old_string with new_string.
    :param root_directory: The directory to start searching from.
    :param old_string: The string in the filename to be replaced.
    :param new_string: The string to replace with
"""

import os

def rename_files(root_directory, old_string, new_string):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if old_string in filename:
                new_filename = filename.replace(old_string, new_string)
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_filename)

                print(f"Renaming '{old_file_path}' to '{new_file_path}'")
                os.rename(old_file_path, new_file_path)

# Example Usage
root_dir = 'D:/WTPyScripts/input' # Replace with your directory path
old_str = 'OLD' # Replace with the text you want to replace
new_str = 'NEW' # Replace with the new text

rename_files(root_dir, old_str, new_str)
