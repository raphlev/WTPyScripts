#!/usr/bin/env python3
r"""
scan_files_pattern.py

This script scans files with a specified extension in a given directory (including subdirectories)
and searches for lines matching a specified pattern. The pattern can include wildcards '*'
and a negation character '!'. It writes all unique matching lines to an output file.

Features:
- **Encoding Detection**: Attempts to detect the encoding of each file to handle files with different encodings.
- **Pattern Matching**: Supports wildcards '*' and negation '!' in the search pattern.
  - Wildcards '*' are converted to '.*' in regular expressions.
  - The '!' character is used to specify patterns that should **not** be included in the matching lines.
- **Command Line Usage**: Allows specifying the input directory, output file, file extension, and search pattern via command-line arguments.
- **Examples of Usage Not Related to Import Statements**: See below for examples of how to use the script for various patterns.

---

### Encoding Detection:
- The script uses the `chardet` library (if installed) to detect file encodings.
- If `chardet` is not available or fails to detect the encoding, it tries common encodings like `utf-8`, `latin-1`, and `cp1252`.
- If the encoding cannot be determined, the file is skipped.

### Pattern Matching: 
- The pattern is structured as: include_pattern!exclude_pattern1|exclude_pattern2|...
- The search pattern can include:
  - **Wildcards `*`**: Converted to `.*` in the regular expression to match any sequence of characters.
  - **Negation `!`**: Splits the pattern into an include pattern and an exclude pattern.
    - The part before '!' is the **include pattern** include_pattern
    - The part after '!' split by | is the list of **exclude patterns** exclude_pattern1|exclude_pattern2|...
    - Lines matching the include pattern but **not** matching any of the exclude patterns will be included.
- All other characters in the pattern are escaped to prevent unintended regex behavior.
- The search is case-insensitive.

### Case sensitivity of the inclusion and exclusion patterns:
    --include-ignore-case: Makes the inclusion pattern case-insensitive.
    --exclude-ignore-case: Makes the exclusion pattern case-insensitive.
    Default Behavior: if flags not provided, both inclusion and exclusion patterns are case-sensitive unless the respective flag is provided.
    Usage: Use the flags to control the case sensitivity according to your needs.

### Dependencies:
  - Python 3.x
  - chardet (optional, for encoding detection)

### Command Line Usage:
- To run the script, use the following command:

  ```bash
  python scan_files_pattern.py --inputDir/-i inputDir --outputFile/-o outputFile.txt --pattern "your_pattern_here" --file-extension "file_extension_here" --log-level "log_level_here"

  python scan_files_pattern.py -i "D:\EclipseWorkspace\Indigo3210.3302" -o "C:\Users\levequer\Downloads\outputFileScan.txt" --pattern "import *s1000D*" --file-extension "java" --log-level INFO 

  python scan_files_pattern.py -i "D:\EclipseWorkspace\Indigo3210.3302" -o "C:\Users\levequer\Downloads\outputFileScan.txt" --pattern "import *!S1000D|com.indigo|com.ptc.wvs" --file-extension "java" --log-level INFO --include-ignore-case --exclude-ignore-case
    INFO: Successfully wrote 1032 lines to 'C:\Users\levequer\Downloads\outputFileScan.txt'.
  python scan_files_pattern.py -i "D:\EclipseWorkspace\Indigo3210.3302" -o "C:\Users\levequer\Downloads\outputFileScan.txt" --pattern "import *!S1000D|com.indigo|com.ptc.wvs" --file-extension "java" --log-level INFO                                            
    INFO: Successfully wrote 1048 lines to 'C:\Users\levequer\Downloads\outputFileScan.txt'.

  ```

### Examples:

Find all lines starting with import and containing s1000D:
python.exe .\scan_files_pattern.py -i "D:\EclipseWorkspace\Indigo3210.3302" -o "C:\Users\levequer\Downloads\outputFileScan.txt" --pattern "import *s1000D*" --file-extension "java" --log-level INFO 

Find all lines starting with import and containing s1000D but excluding those containing com.indigo:
python scan_files_pattern.py --inputDir "." --outputFile "output.txt" --pattern "import *S1000d*!*come.indigo*" --file-extension "java" --log-level INFO
Equivalent to:
python scan_files_pattern.py --inputDir "." --outputFile "output.txt" --pattern "import *S1000d*!com.indigo" --file-extension "java" --log-level INFO

Find all lines starting with import and containing s1000D but excluding those containing com.indigo: and those containing com.ptc.wvs
python scan_files_pattern.py -i "D:\EclipseWorkspace\Indigo3210.3302" -o "C:\Users\levequer\Downloads\outputFileScan.txt" --pattern "import *!s1000D|com.indigo|com.ptc.wvs" --file-extension "java" --log-level INFO

Find all lines containing TODO comments in Python files:
python scan_files_pattern.py ./MyPythonProject todos_output.txt --pattern "*TODO*" --file-extension "py"

Find all lines starting with import but excluding those containing s1000D:
python scan_files_pattern.py ./MyJavaProject imports_without_s1000D.txt --pattern "import *!*s1000D*" --file-extension "java"

Find all lines containing System.out.println but not containing debug:
python scan_files_pattern.py ./MyJavaProject println_statements.txt --pattern "*System.out.println(*!*debug*" --file-extension "java"

Find all class definitions that are not interfaces:
python scan_files_pattern.py ./MyJavaProject classes_not_interfaces.txt --pattern "class *!*interface *" --file-extension "java"

Find all lines with annotations except those with @Override:
python scan_files_pattern.py ./MyJavaProject annotations.txt --pattern "@*" --pattern "!@Override*" --file-extension "java"

Find all lines using a deprecated method oldMethod but not containing ignoreThis:
python scan_files_pattern.py ./MyJavaProject deprecated_usage.txt --pattern "*oldMethod(*!*ignoreThis*" --file-extension "java"

Find all lines containing a specific annotation @Deprecated but not @Deprecated(since="1.5"):
python scan_files_pattern.py ./MyJavaProject deprecated_annotations.txt --pattern "*@Deprecated*!*since=\"1.5\"*" --file-extension "java"

Find all lines defining public classes but exclude those with Test in the name:
python scan_files_pattern.py ./MyJavaProject public_classes.txt --pattern "public *class *!*Test*" --file-extension "java"


"""

import os
import re
import argparse
import logging

try:
    import chardet
except ImportError:
    chardet = None

def detect_encoding(file_path):
    """
    Detects the encoding of a file.
    """
    if chardet:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            if encoding:
                return encoding
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                file.readline()
            return encoding
        except UnicodeDecodeError:
            continue
    return None

def wildcard_to_regex(pattern):
    """
    Converts a wildcard pattern to a regular expression pattern.
    """
    escaped_pattern = ''
    for char in pattern:
        if char == '*':
            escaped_pattern += '.*'
        elif char == '|':
            escaped_pattern += '|'
        else:
            escaped_pattern += re.escape(char)
    return escaped_pattern

def find_pattern_in_files(directory, search_pattern, file_extension, include_ignore_case, exclude_ignore_case):
    """
    Recursively searches for lines matching the search pattern in files with the specified extension.
    """
    if '!' in search_pattern:
        include_part, exclude_part = search_pattern.split('!', 1)
        include_regex_pattern = wildcard_to_regex(include_part)
        exclude_regex_pattern = wildcard_to_regex(exclude_part)

        # Compile inclusion regex with or without IGNORECASE
        if include_ignore_case:
            include_regex = re.compile(include_regex_pattern, re.IGNORECASE)
        else:
            include_regex = re.compile(include_regex_pattern)

        # Compile exclusion regex with or without IGNORECASE
        if exclude_ignore_case:
            exclude_regex = re.compile(exclude_regex_pattern, re.IGNORECASE)
        else:
            exclude_regex = re.compile(exclude_regex_pattern)
    else:
        include_regex_pattern = wildcard_to_regex(search_pattern)

        # Compile inclusion regex with or without IGNORECASE
        if include_ignore_case:
            include_regex = re.compile(include_regex_pattern, re.IGNORECASE)
        else:
            include_regex = re.compile(include_regex_pattern)

        exclude_regex = None

    unique_lines = set()

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.' + file_extension):
                file_path = os.path.join(root, filename)
                encoding = detect_encoding(file_path)
                if not encoding:
                    logging.warning(f"Could not determine encoding for {file_path}. Skipping file.")
                    continue
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        for line in file:
                            if include_regex.match(line):
                                if exclude_regex is None or not exclude_regex.search(line):
                                    matching_line = line.rstrip('\n')
                                    unique_lines.add(matching_line)
                except Exception as e:
                    logging.error(f"Error reading file {file_path}: {e}")

    return sorted(unique_lines, key=lambda s: s.lower())

def write_lines_to_file(lines_list, output_file):
    """
    Writes the list of lines to the specified output file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for line in lines_list:
                file.write(f"{line}\n")
        logging.info(f"Successfully wrote {len(lines_list)} lines to '{output_file}'.")
    except Exception as e:
        logging.error(f"Error writing to file {output_file}: {e}")

def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Scan files for lines containing a specific pattern.'
    )
    parser.add_argument(
        '--inputDir',
        '-i',
        required=True,
        help='The input directory to scan for files.'
    )
    parser.add_argument(
        '--outputFile',
        '-o',
        required=True,
        help='The output file to write the lines containing the pattern.'
    )
    parser.add_argument(
        '--pattern',
        default='import *s1000D*',
        help='The pattern to look for in the lines. Wildcards (*) and negation (!) are supported.'
    )
    parser.add_argument(
        '--file-extension',
        default='java',
        help='The file extension to scan for. Default is "java".'
    )
    parser.add_argument(
        '--include-ignore-case',
        action='store_true',
        help='Make the inclusion pattern case-insensitive.'
    )
    parser.add_argument(
        '--exclude-ignore-case',
        action='store_true',
        help='Make the exclusion pattern case-insensitive.'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level. Default is "INFO".'
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Configure logging
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    logging.basicConfig(level=numeric_level, format='%(levelname)s: %(message)s')

    # Suppress chardet debug messages unless log level is DEBUG
    if numeric_level > logging.DEBUG:
        logging.getLogger('chardet').setLevel(logging.WARNING)

    lines_list = find_pattern_in_files(
        args.inputDir,
        args.pattern,
        args.file_extension,
        args.include_ignore_case,
        args.exclude_ignore_case
    )
    write_lines_to_file(lines_list, args.outputFile)

if __name__ == '__main__':
    main()
