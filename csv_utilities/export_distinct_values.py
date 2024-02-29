"""
Export Unique Values from CSV Based on Column Position

This script reads from a specified input CSV file, extracts unique values from a specified column,
and outputs these unique values along with their occurrence counts to a new CSV file. The column
from which values are extracted is determined by a user-provided position argument. 
Empty values in the specified column are replaced with "NULL" in the output.

Configuration:
- The script uses a semicolon (';') as the delimiter for both reading from the input file and writing to the output file.

Usage:
python script.py -i <input_csv_file_path> -o <output_csv_file_path> -p <column_position>

Where:
- <input_csv_file_path> is the path to the CSV file from which to read data.
- <output_csv_file_path> is the path where the CSV file with unique values and their counts will be saved.
- <column_position> is the 1-based index of the column from which to extract unique values.

Example:
python script.py -i "data/input_data.csv" -o "results/unique_values.csv" -p 8

This will read from 'data/input_data.csv', extract unique values from the 8th column, count occurrences,
replace any empty values with "NULL", and then write the unique values and their counts to 'results/unique_values.csv'.

Author: Raphael Leveque, Feb 2024
"""

import csv
import argparse

def export_distinct_values(input_csv, output_csv, position):
    # Convert the human-friendly position to zero-based index
    index = position - 1
    
    # Dictionary to hold the value and count of occurrences for each unique value
    value_counts = {}

    try:
        with open(input_csv, mode='r', encoding='utf-8') as infile:
            print(f"Reading from {input_csv}")
            reader = csv.reader(infile, delimiter=';')
            next(reader, None)  # Skip the header row
            for row in reader:
                if len(row) > index:  # Ensure the row has enough elements
                    # Treat the value as text, even if it looks like a number
                    value = row[index]
                    # Replace empty value with "NULL"
                    value = value if value.strip() else "NULL"
                    # Count occurrences of each value
                    if value in value_counts:
                        value_counts[value] += 1
                    else:
                        value_counts[value] = 1

        # Sort values alphabetically and prepare them for writing
        sorted_values_counts = sorted(value_counts.items())

        with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
            print(f"Writing to {output_csv}")
            writer = csv.writer(outfile, delimiter=';')  # Keep ";" as the delimiter
            writer.writerow(['Value', 'Count'])  # Header for value and count
            for value, count in sorted_values_counts:
                writer.writerow([value, count])

        print("File has been written successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Export unique values from a CSV file based on position, ensuring no duplicates.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')
    parser.add_argument('-p', '--position', required=True, type=int, help='Position of the value in the CSV (1-based index)')

    args = parser.parse_args()
    export_distinct_values(args.input, args.output, args.position)

if __name__ == "__main__":
    main()
