"""
Script Purpose: Extracts properties of enumerated values from an XML file and generates an output CSV file.
Each enumerated value's properties, such as name, displayName, selectable, and sort_order, including their
csvisDefault and csvvalue, are captured and written to the CSV with '~' as the delimiter.

Developer: Raphael Leveque
"""

import csv
import xml.etree.ElementTree as ET
import sys

def extract_enumerated_values_properties(xml_file_path):
    """
    Extracts properties of enumerated values from the provided XML file.
    
    Parameters:
        xml_file_path (str): Path to the XML file.
        
    Returns:
        list of dicts: List containing dictionaries of properties for each enumerated value.
    """
    try:
        tree = ET.parse(xml_file_path)
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        sys.exit(1)
        
    root = tree.getroot()
    enumerated_values = []
    current_enum = None

    for elem in root.iter():
        if elem.tag == 'csvBeginEnumMemberView':
            current_enum = {
                'name': elem.find('csvname').text,
                'displayName csvisDefault': '',
                'displayName csvvalue': '',
                'selectable csvisDefault': '',
                'selectable csvvalue': '',
                'sort_order csvisDefault': '',
                'sort_order csvvalue': '',
            }
        elif elem.tag == 'csvPropertyValue' and current_enum is not None:
            prop_name = elem.find('csvname').text
            csvisDefault = elem.find('csvisDefault').text if elem.find('csvisDefault') is not None else ''
            csvvalue = elem.find('csvvalue').text if elem.find('csvvalue') is not None else ''
            current_enum[f'{prop_name} csvisDefault'] = csvisDefault
            current_enum[f'{prop_name} csvvalue'] = csvvalue
        elif elem.tag == 'csvEndEnumMemberView' and current_enum is not None:
            enumerated_values.append(current_enum)
            current_enum = None

    return enumerated_values

def write_to_csv(enumerated_values, output_csv_file_path):
    """
    Writes the extracted enumerated values to a CSV file.
    
    Parameters:
        enumerated_values (list of dicts): Extracted properties of enumerated values.
        output_csv_file_path (str): Path to the output CSV file.
    """
    try:
        with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            if enumerated_values:
                fieldnames = enumerated_values[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='~')
                writer.writeheader()
                for enum_val in enumerated_values:
                    writer.writerow(enum_val)
            else:
                print("No enumerated values were extracted from the XML.")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py path_to_xml_file path_to_output_csv_file")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    output_csv_file_path = sys.argv[2]

    enumerated_values = extract_enumerated_values_properties(xml_file_path)
    write_to_csv(enumerated_values, output_csv_file_path)
    print(f"CSV file has been successfully created at {output_csv_file_path}")

if __name__ == "__main__":
    main()
