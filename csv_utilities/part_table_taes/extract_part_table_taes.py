import sys
import re

def process_file(input_file, output_file):
    """
    Process the input file to extract electronic part information,
    ensuring no duplicate taes_numbers and that entries are sorted by taes_number.
    Author: xxx

    Args:
    input_file (str): Path to the input file.
    output_file (str): Path to the output CSV file.
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        headers = []
        part_name = ''
        processing_part = False
        entries = {}
        sep_input_file = '|'
        sep_output_file = ';'
        # write header output file
        outfile.write('taes_number'+sep_output_file+'HDLSChematicSymbol'+sep_output_file+'AllegroFootprint'+'AltSymbols\n')

        for line in infile:
            if 'PART ' in line:
                part_name = re.search(r"PART '([^']+)'", line).group(1)
                processing_part = True
                values_buffer = []
            elif processing_part and line.startswith(':'):
                headers = line.strip(':;\n').split(sep_input_file)
            elif processing_part and 'END_PART' in line:
                for values_line in values_buffer:
                    # Split values using the sep_input_file separator first and removing ' at beginning and ' at the end
                    raw_values = values_line.split(sep_input_file)
                    #values = [re.search(r"'(.*)'", val).group(1) if re.search(r"'(.*)'", val) else '' for val in raw_values]
                    values = []
                    for val in raw_values:
                        found = re.search(r"'(.*)'", val)
                        if found:
                            values.append(found.group(1))
                        else:
                            values.append('')  # Append empty string if no match

                   # Correcting the specific handling of the ACCESSOIRE field
                    acc_index = headers.index("ACCESSOIRE (OPT='-')=PART_NUMBER")
                    # Regex to extract everything after the last single quote in the specific field
                    # TBD: solution1, solution2, or which solution?
                    # solution1: keep full value to avoid duplicates with ACCESSOIRE SOCKET, SUPCCJ32_SANS_PIONS,  etc..
                    values[acc_index] = re.sub("-'='", "", values[acc_index])
                    # solution2: keep only last PART_NUMBER but contains duplicates, see log
                    #values[acc_index] = re.search(r"'.*?'([^']*)$", values[acc_index]).group(1)
                    
                    if len(values) != len(headers):
                        print(f"Data mismatch in headers and values for part {part_name}: Expected {len(headers)}, found {len(values)}")
                        print(f"Headers: {headers}")
                        print(f"Values: {values}")
                        continue

                    data = dict(zip(headers, values))
                    try:
                        taes_number = data['ACCESSOIRE (OPT=\'-\')=PART_NUMBER']
                        if taes_number in entries:
                            print(f"Warning: Duplicate taes_number '{taes_number}' found. Not added to output.")
                        else:
                            entry = f"{taes_number}{sep_output_file}{part_name}{sep_output_file}{data['JEDEC_TYPE']}{sep_output_file}{data['ALT_SYMBOLS'].strip('()')}\n"
                            entries[taes_number] = entry
                    except KeyError as e:
                        print(f"Key error: {e} in part {part_name}")

                processing_part = False
                values_buffer = []

            elif processing_part and not line.strip().endswith(';'):
                values_buffer.append(line.strip())

        # Write sorted entries by taes_number
        #for entry in sorted(entries.values()):
        #    outfile.write(entry)
        for taes_number in sorted(entries):#by default sorts the dictionary by its keys
            outfile.write(entries[taes_number])

        print("Processing complete.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input.ptf> <output.csv>")
        print("Example: python.exe .\extract_part_table_taes.py .\part_table_taes_16022024_test.ptf .\output.csv")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    process_file(input_path, output_path)
