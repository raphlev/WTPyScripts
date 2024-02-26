"""
File: merge_xml_enumerated_values_with_new_entries.py
Author: Raphael Leveque
Date: February, 2024
Description: Merge XML and CSV enumeration definitions.
options:
  -h, --help            show this help message and exit
  -i INPUT_XML_FILE, --input_xml_file INPUT_XML_FILE
                        Path to the input XML file.
  -n NEW_ENTRIES_CSV_FILE, --new_entries_csv_file NEW_ENTRIES_CSV_FILE
                        Path to the CSV file with new entries.
  -o OUTPUT_XML_FILE, --output_xml_file OUTPUT_XML_FILE
                        Path for the output XML file.
  -s {name,displayName}, --sort_by {name,displayName}
                        OPTIONAL (default is 'name') Sort entries by 'name' or 'displayName'.
  -p, --preserve_original_order
                        OPTIONAL (if -p not used, reorder all entries per name) Preserve the original order of entries & appending    
                        new ones at the end
1°) This script merges enumeration definitions from an XML file with new entries from a CSV file, then outputs the updated enumeration to a new file. It supports sorting by name or displayName, and optionally preserves the original order of existing entries.
- Input XML Enumerated Values: contains one EnumDefView entry with occurrences of EnumMemberView members (export file of enumerated values from Windchill)
- Input CSV file: csv file with header row [name~displayName~csvlocale_fr] of new enumeration members to insert into xml file
- Output file: list of merged EnumMemberView members in a text file which can be used to replace original XML Enumerated Values
2°) It also support management of duplicates and output additional log files
- extracted_data.txt: logs input xml file content into csv and json
- extracted_new_entries.txt: logs input csv file into csv
- duplicates_against_new_entries.txt: logs duplicates (name as key) found within csv input file
- duplicates_against_existing.txt: logs duplicates (name as key) found in xml input file against csv input file

List ([]):
Ordered: Maintains the order in which elements are added.
Mutable: You can change, add, or remove items.
Allows duplicates: Multiple elements can have the same value.

Set (set()):
Unordered: Does not maintain the order of elements.
Mutable: You can add or remove items, but you can't change them.
No duplicates: Each element must be unique.

Dictionary ({}):
Unordered (before Python 3.7, but ordered by insertion order from Python 3.7+): Does not maintain order traditionally, but in recent versions of Python, it retains the order of insertion.
Mutable: You can add, remove, or change items.
Key-Value pairs: Stores data as key-value pairs where each key must be unique.

"""

import csv
import argparse
from lxml import etree
import json

def normalize_xml(xml_content):
    replacements = [
            ('</csvBeginEnumDefView>', ''),
            ('</csvBeginEnumMemberView>', ''),
            ('<csvEndEnumMemberView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessEnumMembership"/>', '</csvBeginEnumMemberView>'),
            ('<csvEndEnumMemberView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumMembership"/>', '</csvBeginEnumMemberView>'),
            ('<csvEndEnumDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessEnumerationDefinition"/>', '</csvBeginEnumDefView>'),
            ('<csvEndEnumDefView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumerationDefinition"/>', '</csvBeginEnumDefView>'),
    ]
    for old, new in replacements:
        xml_content = xml_content.replace(old, new)
    return xml_content

def parse_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()

    normalized_xml = normalize_xml(xml_content)
    root = etree.fromstring(normalized_xml.encode('utf-8'))

    extracted_data = []

    for enum_member in root.xpath("//csvBeginEnumMemberView"):
        name = enum_member.xpath("./csvname/text()")[0]
        displayName = enum_member.xpath(".//csvPropertyValue[csvname='displayName']/csvvalue/text()")
        displayName = displayName[0] if displayName else ''
        selectable = enum_member.xpath(".//csvPropertyValue[csvname='selectable']/csvvalue/text()")
        selectable = selectable[0] if selectable else ''
        sort_order = enum_member.xpath(".//csvPropertyValue[csvname='sort_order']/csvvalue/text()")
        sort_order = sort_order[0] if sort_order else ''
        locale_fr = enum_member.xpath(".//csvPropertyValue[csvname='displayName']/csvlocale_fr/text()")
        locale_fr = locale_fr[0] if locale_fr else ''

        extracted_data.append({
            'name': name,
            'displayName': displayName,
            'selectable': selectable,
            'sort_order': sort_order,
            'csvlocale_fr': locale_fr
        })

    with open('extracted_data.txt', 'w', encoding='utf-8') as f:
            f.write('name~displayName~selectable~sort_order~csvlocale_fr\n')  # Write header
            for entry in extracted_data:
                f.write(f"{entry['name']}~{entry['displayName']}~{entry['selectable']}~{entry['sort_order']}~{entry['csvlocale_fr']}\n")
            json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    return extracted_data

def read_new_entries(csv_file_path):
    expected_columns = ['name', 'displayName', 'csvlocale_fr']
    new_entries = []
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='~')
            if not all(column in reader.fieldnames for column in expected_columns):
                raise ValueError("CSV file format is incorrect. Expected columns: " + ", ".join(expected_columns))
            else:
                for row in reader:
                    new_entries.append({
                    'name': row['name'],
                    'displayName': row['displayName'],
                    'csvlocale_fr': row.get('csvlocale_fr', '')  # Provide a default value if column is missing
                })
    except UnicodeDecodeError:
        raise UnicodeDecodeError("Failed to decode the CSV file. Please check the file encoding. UTF-16 was attempted.")


    with open('extracted_new_entries.txt', 'w', encoding='utf-8') as f:
        f.write('name~displayName~csvlocale_fr\n')  # Write header
        for entry in new_entries:
            csvlocale_fr = entry.get('csvlocale_fr', '')
            f.write(f"{entry['name']}~{entry['displayName']}~{csvlocale_fr}\n")

    return new_entries

def remove_duplicates_against_new_entries(entries):
    seen = set()
    unique_entries = []
    duplicates = []
    for entry in entries:
        if entry['name'] in seen:
            duplicates.append(entry)
        else:
            seen.add(entry['name'])
            unique_entries.append(entry)
    return unique_entries, duplicates

def remove_duplicates_against_existing(existing_entries, new_entries):
    existing_names = {entry['name']: entry for entry in existing_entries}
    unique_new_entries = []
    duplicates = []
    updated_entries = []  # To keep track of entries updated from selectable: False to True

    for entry in new_entries:
        if entry['name'] in existing_names:
            duplicates.append(entry)
            # Check if we need to update the 'selectable' field to true
            if existing_names[entry['name']].get('selectable') == 'false':
                existing_names[entry['name']]['selectable'] = 'true'
                updated_entries.append(existing_names[entry['name']])
        else:
            unique_new_entries.append(entry)

    # Optionally, log the updated entries
    if updated_entries:
        with open('updated_selectable_entries.txt', 'w', encoding='utf-8') as file:
            for updated_entry in updated_entries:
                file.write(f"{updated_entry['name']}: selectable updated to True\n")

    return unique_new_entries, duplicates, list(existing_names.values())

def log_duplicates(duplicates, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for duplicate in duplicates:
            file.write(f"{duplicate['name']}\n")  # Logging only the name for simplicity
            file.write(json.dumps(duplicate, ensure_ascii=False) + "\n")

def generate_output(existing_entries, new_entries, output_file_path, sort_by, preserve_order):
    # Step 1: Remove duplicates within new_entries
    new_entries, duplicates_against_new_entries = remove_duplicates_against_new_entries(new_entries)
    log_duplicates(duplicates_against_new_entries, 'duplicates_against_new_entries.txt')

    # Step 2: Remove duplicates against existing_entries and update existing_entries if needed
    unique_new_entries, duplicates_against_existing, updated_existing_entries = remove_duplicates_against_existing(existing_entries, new_entries)
    log_duplicates(duplicates_against_existing, 'duplicates_against_existing.txt')

    # Use the updated_existing_entries list for further processing
    existing_entries = updated_existing_entries

    # Combine unique new entries with updated existing entries
    combined_entries = existing_entries + unique_new_entries

    # Sort combined entries based on the sort_by argument
    if sort_by not in ['name', 'displayName']:
        raise ValueError("sort_by argument must be 'name' or 'displayName'")
    sorted_combined_entries = sorted(combined_entries, key=lambda x: x[sort_by].lower())

    # Update sort_order based on sorted position
    for index, entry in enumerate(sorted_combined_entries):
        entry['sort_order'] = str(index)

    # Map to quickly find updated sort_order
    #map_sort_order = {entry['name']: entry['sort_order'] for entry in sorted_combined_entries}
    # Update the sort_order in the original combined list based on the mapping
    #for entry in combined_entries:
    #    entry['sort_order'] = map_sort_order[entry['name']]

    # If not preserving order, sort entries by name for the output
    if not preserve_order:
        combined_entries = sorted(combined_entries, key=lambda x: x['name'].lower())

    # Writing to file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for entry in combined_entries:
            file.write(format_entry_block(entry) + "\n")

def format_entry_block(entry_details):
    # Always include 'selectable' with a default of "true" if not specified
    selectable_value = entry_details.get('selectable', 'true')

    # Replace '&' with '&amp;' in 'displayName' and 'csvlocale_fr' for XML encoding
    displayName = entry_details.get('displayName', '').replace('&', '&amp;')
    csvlocale_fr = entry_details.get('csvlocale_fr', '').replace('&', '&amp;')

    # Conditionally include the 'csvlocale_fr' tag
    csvlocale_fr_tag = f'\n      <csvlocale_fr>{csvlocale_fr}</csvlocale_fr>' if csvlocale_fr else ''

    # Construct the entry block with explicit indentation for each line
    entry_block = f'''   <csvBeginEnumMemberView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.beginProcessEnumMembership">
      <csvname>{entry_details['name']}</csvname>
   </csvBeginEnumMemberView>
   <csvPropertyValue handler="com.ptc.core.lwc.server.BaseDefinitionLoader.processEnumEntryPropertyValue">
      <csvname>displayName</csvname>
      <csvisDefault>false</csvisDefault>
      <csvvalue>{displayName}</csvvalue>{csvlocale_fr_tag}
   </csvPropertyValue>
   <csvPropertyValue handler="com.ptc.core.lwc.server.BaseDefinitionLoader.processEnumEntryPropertyValue">
      <csvname>selectable</csvname>
      <csvisDefault>false</csvisDefault>
      <csvvalue>{entry_details.get('selectable', 'true')}</csvvalue>
   </csvPropertyValue>
   <csvPropertyValue handler="com.ptc.core.lwc.server.BaseDefinitionLoader.processEnumMembershipPropertyValue">
      <csvname>sort_order</csvname>
      <csvisDefault>false</csvisDefault>
      <csvvalue>{entry_details['sort_order']}</csvvalue>
   </csvPropertyValue>
   <csvEndEnumMemberView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumMembership"/>'''

    # No additional processing needed for indentation
    return entry_block

def main():
    parser = argparse.ArgumentParser(description='Merge XML and CSV enumeration definitions.')
    parser.add_argument('-i', '--input_xml_file', type=str, required=True, help='Path to the input XML file.')
    parser.add_argument('-n', '--new_entries_csv_file', type=str, required=True, help='Path to the CSV file with new entries.')
    parser.add_argument('-o', '--output_xml_file', type=str, required=True, help='Path for the output XML file.')
    parser.add_argument('-s', '--sort_by', type=str, choices=['name', 'displayName'], default='name', help="OPTIONAL (default is 'name') Sort entries by 'name' or 'displayName'.")
    parser.add_argument('-p', '--preserve_original_order', action='store_true', help="OPTIONAL (if -p not used, reorder all entries per name) Preserve the original order of entries & appending new ones at the end")
    
    args = parser.parse_args()

    existing_entries = parse_xml(args.input_xml_file)
    new_entries = read_new_entries(args.new_entries_csv_file)
    generate_output(existing_entries, new_entries, args.output_xml_file, args.sort_by, args.preserve_original_order)

if __name__ == "__main__":
    main()
