import pandas as pd
import random
import string
import os

def is_number(s):
    """Check if the input is a number (integer or float)."""
    try:
        float(s)
        return True
    except ValueError:
        return False

def random_number_string(length, is_float):
    """Generate a random number string of the specified length."""
    if is_float:
        return "{:.{}f}".format(random.random(), length - 2)  # length - 2 to account for '0.'
    else:
        return str(random.randint(10**(length-1), (10**length)-1))


def anonymize_excel(file_path, output_file_path):
    try:
        # Check if the output file exists to set the correct mode
        file_exists = os.path.exists(output_file_path)

        # Delete the output file if it exists
        if file_exists:
            os.remove(output_file_path)
            print(f"Existing output file '{output_file_path}' deleted.")

        # Load the Excel file
        print("Loading the Excel file...")
        excel_file = pd.ExcelFile(file_path)

        # Process each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            start_row = 1 if excel_file.sheet_names.index(sheet_name) == 0 else 2
            non_empty_columns = df.dropna(axis=1, how='all').columns

            for col in non_empty_columns:
                if excel_file.sheet_names.index(sheet_name) == 0 and col == df.columns[0]:
                    continue  # Skip the first column of the first sheet
                for row in range(start_row, len(df)):
                    cell_value = df.at[row, col]
                    if pd.notna(cell_value):
                        if is_number(cell_value):
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
