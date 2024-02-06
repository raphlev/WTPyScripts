"""
Export Unique Revisions from CSV

This script reads a CSV file, extracts unique revisions for the first occurrence of each reference,
and exports these revisions to a new CSV file in alphabetical order (numbers first, then letters).

Configuration:
- Delimiter used in the input CSV: '|'
- Index for 'Reference' column: 0 (first column)
- Index for 'Revision' column: 6 (seventh column, adjust if your CSV structure differs)
- Author: Raphael Leveque

Usage:
python script.py -i <input_csv_file_path> -o <output_csv_file_path>
"""

import csv
import argparse

def export_unique_revisions(input_csv, output_csv):
    unique_references = set()
    unique_revisions = set()

    try:
        with open(input_csv, mode='r', encoding='utf-8') as infile:
            print(f"Reading from {input_csv}")
            reader = csv.reader(infile, delimiter='|')  # Ensure this matches your CSV delimiter
            next(reader, None)  # Skip the header row if your CSV file has one
            for row in reader:
                if len(row) > 6:  # Ensure the row has enough columns to access the revision
                    reference = row[0]
                    revision = row[6]
                    if reference not in unique_references:
                        unique_references.add(reference)
                        if revision not in unique_revisions:
                            unique_revisions.add(revision)
                else:
                    print(f"Skipping row due to insufficient columns: {row}")

        # Sort the revisions alphabetically before writing to the output file
        sorted_revisions = sorted(list(unique_revisions))

        with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
            print(f"Writing to {output_csv}")
            writer = csv.writer(outfile)
            #writer.writerow(['Revision'])
            for revision in sorted_revisions:
                writer.writerow([revision])

        print("File has been written successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Export unique revisions from a CSV file.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file path')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file path')

    args = parser.parse_args()
    export_unique_revisions(args.input, args.output)

if __name__ == "__main__":
    main()
