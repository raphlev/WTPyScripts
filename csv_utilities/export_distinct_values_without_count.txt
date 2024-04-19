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
