"""
File: excel_data_anonymizer.py
Author: Raphael Leveque
Date: January , 2024
Description: this script takes in an excel file, and anonymizes its content values. Specific rules related to source excel file are added (see comments in code). Number, Date and String types are considered to generate fake values of same type and same size.
"""

import pandas as pd
import random
import string
import os
from datetime import datetime, timedelta

def is_number(s):
    """Check if the input is a number (integer or float)."""
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_date(cell):
    """Check if the cell value is a date."""
    if isinstance(cell, datetime):
        return True
    try:
        pd.to_datetime(cell)
        return True
    except:
        return False

def random_number_string(length, is_float):
    """Generate a random number string of the specified length."""
    if is_float:
        return "{:.{}f}".format(random.random(), length - 2)  # length - 2 to account for '0.'
    else:
        return str(random.randint(10**(length-1), (10**length)-1))

def update_date(cell):
    """Update the date by adding one day."""
    date = pd.to_datetime(cell)
    updated_date = date + timedelta(days=1)
    return updated_date

def anonymize_excel(file_path, output_file_path):
    try:
        # Delete the output file if it exists
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
            print(f"Existing output file '{output_file_path}' deleted.")

        # Load the Excel file
        print("Loading the Excel file...")
        excel_file = pd.ExcelFile(file_path)

        # Process each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Determine the starting row
            if sheet_name == "Export":
                start_row = 0  # For 'Export' sheet, start from row 3 (index 2)
            else:
                start_row = 1  # For other sheets, start from row 4 (index 3)

            non_empty_columns = df.dropna(axis=1, how='all').columns

            for col in non_empty_columns:
                if sheet_name == "Export" and col == df.columns[0]:
                    continue  # Skip the first column of the 'Export' sheet
                for row in range(start_row, len(df)):
                    cell_value = df.at[row, col]
                    if pd.notna(cell_value):
                        if is_date(cell_value):
                            df.at[row, col] = update_date(cell_value)
                        elif is_number(cell_value):
                            # Keep numbers with same size, change values
                            cell_str = str(cell_value)
                            is_float = '.' in cell_str
                            df.at[row, col] = random_number_string(len(cell_str), is_float)
                        else:
                            # Generate a random string of the same length for non-numbers
                            df.at[row, col] = ''.join(random.choices(string.ascii_letters + string.digits, k=len(str(cell_value))))

            # Save the modified DataFrame to the file
            if file_exists:
                with pd.ExcelWriter(output_file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                with pd.ExcelWriter(output_file_path, mode='w', engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                file_exists = True  # Set file_exists to True for subsequent iterations

        print("Anonymization complete.")
    except Exception as e:
        print(f"An error occurred: {e}")


input_file = 'D:/WTPyScripts/input/other/P0.xlsx'
output_file = 'D:/WTPyScripts/input/other/P0_NEW.xlsx'
# Replace with actual file paths
anonymize_excel(input_file, output_file)
