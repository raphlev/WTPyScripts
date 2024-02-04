"""
File: check_corrupted_files.py
Author: Tomasz Krauze
Date: January, 2024
Description: This script is designed to list corrupted Excel sheets

"""

import pandas
import os
import sys
import logging
import os
import warnings
import time

start_time = time.time()
warnings.simplefilter("ignore")
logging.basicConfig(level=logging.INFO)

# Gettting Excels from path provided in first argument
folder_path = sys.argv[1]
files = os.listdir(folder_path)
excel_files = [file for file in files if file.endswith('.xlsx') or file.endswith('.xls')]

if len(sys.argv) != 2:
    print("Usage: python check_corrupted_files.py <path>")
    print("For example: python check_corrupted_files.py C:/Users/xxx/Desktop/excels/src/")
    print("python.exe -m pip install --upgrade pip")
    print("pip install pandas openpyxl xlsxwriter")
    sys.exit(1)

print(f"+------------------------------------------------------------+")
print(f"|        Checking for corrupted files to fix manually        |")
print(f"+------------------------------------------------------------+")

# Loop through each Excel file and extract unique column headers
for file in excel_files:
    
    excel_file_path = os.path.join(folder_path, file)
    print(f"Checking '{excel_file_path}'")

    xls = pandas.ExcelFile(excel_file_path)
    sheet_names = xls.sheet_names

    for sn in (sheet_names):

        # Skip EVVs
        if sn in ('EVVs'):
            continue

        try:

            # Read each sheet into a DataFrame
            df = pandas.read_excel(excel_file_path, sheet_name=sn, header=0, dtype='str', nrows = 1)  # Use the first row as column names

        except (ValueError, TypeError) as e:
            print(f"    Error processing sheet '{sn}' in '{excel_file_path}': {e}")

end_time = time.time()
elapsed_time = round(((end_time - start_time) / 60), 2)
print(f"Total extraction time taken: {elapsed_time} minutes")