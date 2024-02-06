"""
Export Unique Revisions from CSV Based on Oldest "Date Validation"

This script reads a CSV file, identifies each unique reference, and for each reference, it extracts
the revision associated with the oldest "Date Validation". It then exports these unique, oldest revisions
to a new CSV file in alphabetical order, ensuring no duplicates.

Configuration:
- Delimiter used in the input CSV: '|'
- Index for 'Reference' column: 0 (first column)
- Index for 'Revision' column: 6 (seventh column)
- Index for 'Date Validation' column: 10 (eleventh column)
- Author: Raphael Leveque

Usage:
python script.py -i <input_csv_file_path> -o <output_csv_file_path>
"""

import csv
import argparse
from datetime import datetime

def export_unique_revisions(input_csv, output_csv):
    # Dictionary to hold the earliest date validation and corresponding revision for each reference
    reference_data = {}

    try:
        with open(input_csv, mode='r', encoding='utf-8') as infile:
            print(f"Reading from {input_csv}")
            reader = csv.reader(infile, delimiter='|')  # Ensure this matches your CSV delimiter
            next(reader, None)  # Skip the header row
            for row in reader:
                if len(row) > 10:  # Ensure the row has enough columns to access the date
                    reference = row[0]
                    revision = row[6]
                    date_validation_str = row[10]
                    
                    # Attempt to convert date validation to datetime object for comparison
                    try:
                        date_validation = datetime.strptime(date_validation_str, "%d-%b-%Y %H:%M:%S")
                    except ValueError:
                        # Skip rows with invalid date formats
                        print(f"Invalid date format for row: {row}")
                        continue
                    
                    # Check if this is the first occurrence of the reference or if the current date is older
                    if reference not in reference_data or date_validation < reference_data[reference]['date']:
                        # Update reference_data with the current row's revision and date, as it's either
                        # the first occurrence or an older date validation than previously recorded.
                        reference_data[reference] = {'revision': revision, 'date': date_validation}

        # Extract unique revisions, ensuring no duplicates, and sort them alphabetically
        unique_revisions = set(data['revision'] for data in reference_data.values())
        sorted_revisions = sorted(unique_revisions)

        with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
            print(f"Writing to {output_csv}")
            writer = csv.writer(outfile)
            writer.writerow(['Revision'])
            for revision in sorted_revisions:
                writer.writerow([revision])

        print("File has been written successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Export unique revisions from a CSV file based on the oldest "Date Validation", ensuring no duplicates.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')

    args = parser.parse_args()
    export_unique_revisions(args.input, args.output)

if __name__ == "__main__":
    main()
