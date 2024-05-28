"""
Export Unique Values from CSV Based on Column Position or Name with Custom Separator

This script reads from a specified input CSV file, extracts unique values from a specified column
(by position or name), and outputs these unique values to a new CSV file.
Users can specify the column either by its position in the header row (starting by 1) or by its name. 
Empty values in the specified column are replaced with "NULL" in the output. Additionally, the script 
supports specifying a custom field delimiter for both reading the input file and writing to the output file, 
with a default delimiter of ';'.

Usage:
- To specify a column by position and use the default delimiter:
    python script.py -i <input_csv_file_path> -o <output_csv_file_path> -p <column_position>
- To specify a column by name and use a custom delimiter:
    python script.py -i <input_csv_file_path> -o <output_csv_file_path> -n <column_name> -s <delimiter>

Where:
- <input_csv_file_path> is the path to the CSV file from which to read data.
- <output_csv_file_path> is the path where the CSV file with unique values and their counts will be saved.
- <column_position> is the index of the column starting by 1 from which to extract unique values.
- <column_name> is the name of the column from which to extract unique values, as it appears in the header row.
- <delimiter> is the field delimiter to be used for reading the input and writing the output CSV file (optional, default ';').

Examples:
- Using column position with default delimiter:
    python script.py -i "data/input_data.csv" -o "results/unique_values.csv" -p 8
- Using column name with a custom delimiter (e.g., ','):
    python script.py -i "data/input_data.csv" -o "results/unique_values.csv" -n "ColumnName" -s ","

This script provides flexibility in handling CSV files with different structures and delimiters, making it
suitable for a wide range of data extraction tasks.

Author: Raphael Leveque
"""

import csv
import argparse

def export_distinct_values(input_csv, output_csv, position=None, column_name=None, separator=';'):
    index = None
    unique_values = set()  # Use a set to store unique values

    try:
        with open(input_csv, mode='r', encoding='utf-8') as infile:
            print(f"Reading from {input_csv}")
            reader = csv.reader(infile, delimiter=separator)
            header = next(reader)  # Read the header row
            
            if column_name:
                if column_name in header:
                    index = header.index(column_name)
                else:
                    raise ValueError(f"Column name '{column_name}' not found in the header.")
            elif position is not None:
                if 1 <= position <= len(header):
                    index = position - 1  # Convert to zero-based index
                else:
                    raise ValueError(f"Column position {position} is out of range. Please provide a position between 1 and {len(header)}.")

            for row in reader:
                if len(row) > index:
                    value = row[index]
                    value = value if value.strip() else "NULL"
                    unique_values.add(value)  # Add value to the set

        sorted_values = sorted(unique_values)  # Sort the unique values

        with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
            print(f"Writing to {output_csv}")
            writer = csv.writer(outfile, delimiter=separator)
            writer.writerow(['Value'])  # Write header
            for value in sorted_values:
                writer.writerow([value])  # Write each unique value

        print("File has been written successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Export unique values from a CSV file based on column position or name, ensuring no duplicates.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')
    parser.add_argument('-s', '--separator', default=';', help='Field delimiter (default ";")')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--position', type=int, help='Position of the value in the CSV (index starting by 1)')
    group.add_argument('-n', '--name', help='Name of the column')
    
    args = parser.parse_args()
    if args.position:
        export_distinct_values(args.input, args.output, position=args.position, separator=args.separator)
    else:
        export_distinct_values(args.input, args.output, column_name=args.name, separator=args.separator)

if __name__ == "__main__":
    main()
