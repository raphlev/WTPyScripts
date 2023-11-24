import os

def replace_in_files(root_directory, old_string, new_string):
    """
    Recursively replaces old_string with new_string in the contents of files.
    :param root_directory: The directory to start searching from.
    :param old_string: The string in the file contents to be replaced.
    :param new_string: The string to replace with.
    """
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # Read the contents of the file
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()

            # Replace the old string with the new string
            if old_string in contents:
                new_contents = contents.replace(old_string, new_string)

                # Write the new contents back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_contents)
                print(f"Replaced text in '{file_path}'")

# Example Usage
root_dir = 'D:/WTPyScripts/input' # Replace with your directory path
old_str = '>SEP<'  # Replace with the text you want to replace
new_str = '>CUST<'  # Replace with the new text

replace_in_files(root_dir, old_str, new_str)
