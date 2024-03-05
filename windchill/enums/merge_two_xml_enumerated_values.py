"""
File: merge_two_xml_enumerated_values.py
Author: Raphael Leveque
Date: March, 2024
Description: Merge two enumeration definitions.
options:
  -h, --help            show this help message and exit
  -i existing_entries_file, --existing_entries_file EXISTING_ENTRIES_FILE
                        Path to the input XML file.
  -n new_entries_file, --new_entries_file NEW_ENTRIES_FILE
                        Path to the CSV file with new entries.
  -o OUTPUT_XML_FILE, --output_xml_file OUTPUT_XML_FILE
                        Path for the output XML file.
  -s {name,displayName}, --sort_by {name,displayName}
                        OPTIONAL (default is 'name') Sort entries by 'name' or 'displayName'.
  -p, --preserve_original_order
                        OPTIONAL (if -p not used, reorder all entries per name) Preserve the original order of entries & appending    
                        new ones at the end
1°) This script merges enumeration definitions from an "existing" XML file with entries from another "new" XML file, then outputs the updated merged enumeration to a new file. It supports sorting by name or displayName, and optionally preserves the original order of the "existing" XML file entries.
- Input "existing" XML Enumerated Values file: contains one EnumDefView entry with occurrences of EnumMemberView members (export file of enumerated values from Windchill)
- Input "new" XML Enumerated Values file: contains one EnumDefView entry with occurrences of EnumMemberView members (export file of enumerated values from Windchill) to insert into "existing" XML file
- Output file: list of merged EnumMemberView members in a text file which can be used to replace original XML Enumerated Values
2°) It generate additional log files
- existing_entries_log_file.txt: logs input "existing" XML Enumerated Values file
- new_entries_log_file.txt: logs input "new" XML Enumerated Values file

"""

import csv
import argparse
from lxml import etree
import json
import os

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

def parse_xml(entries_file, entries_log_file):
    with open(entries_file, 'r', encoding='utf-8') as file:
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

    log_xml_entries(extracted_data,entries_log_file)

    return extracted_data

def log_xml_entries (entries, filename):
    with open(filename, 'w', encoding='utf-8') as f:
            f.write('name~displayName~selectable~sort_order~csvlocale_fr\n')
            for entry in entries:
                f.write(f"{entry['name']}~{entry['displayName']}~{entry['selectable']}~{entry['sort_order']}~{entry['csvlocale_fr']}\n")
            json.dump(entries, f, ensure_ascii=False, indent=4)

from lxml import etree

def merge_existing_new_entries_to_existing_entries(existing_entries, new_entries):
    # Convert existing entries to a dictionary for faster lookup
    existing_dict = {entry['name']: entry for entry in existing_entries}

    for new_entry in new_entries:
        name = new_entry['name']
        # Check if this new entry exists in the existing entries
        if name in existing_dict:
            # Entry exists, update the specified attributes
            existing_entry = existing_dict[name]
            existing_entry['displayName'] = new_entry.get('displayName', existing_entry.get('displayName'))
            existing_entry['selectable'] = new_entry.get('selectable', existing_entry.get('selectable'))
            existing_entry['sort_order'] = new_entry.get('sort_order', existing_entry.get('sort_order'))
            # Update 'csvlocale_fr' if it exists in the new entry, otherwise keep existing
            if 'csvlocale_fr' in new_entry:
                existing_entry['csvlocale_fr'] = new_entry['csvlocale_fr']
        else:
            # Entry does not exist in the existing entries, add the new entry
            existing_entries.append(new_entry)

    return existing_entries

def generate_output(existing_entries, existing_new_entries, output_folder, sort_by, preserve_order):
    # Combine entries 
    combined_entries = merge_existing_new_entries_to_existing_entries(existing_entries,existing_new_entries)

    # Sort combined entries based on the sort_by argument
    if sort_by not in ['name', 'displayName']:
        raise ValueError("sort_by argument must be 'name' or 'displayName'")
    sorted_combined_entries = sorted(combined_entries, key=lambda x: x[sort_by].lower())

    # Update sort_order based on sorted position
    for index, entry in enumerate(sorted_combined_entries):
        entry['sort_order'] = str(index)

    # If not preserving order, sort entries by name for the output
    if not preserve_order:
        combined_entries = sorted(combined_entries, key=lambda x: x['name'].lower())

    # Writing to file
    output_file_path = os.path.join(output_folder, 'output_merged_file.txt')
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
    parser.add_argument('-i', '--existing_entries_file', type=str, required=True, help='Path to the input XML file.')
    parser.add_argument('-n', '--new_entries_file', type=str, required=True, help='Path to the XML file with new entries.')
    parser.add_argument('-o', '--output_folder', type=str, required=True, help='Path for the output folder.')
    parser.add_argument('-s', '--sort_by', type=str, choices=['name', 'displayName'], default='name', help="OPTIONAL (default is 'name') Sort entries by 'name' or 'displayName'.")
    parser.add_argument('-p', '--preserve_original_order', action='store_true', help="OPTIONAL (if -p not used, reorder all entries per name) Preserve the original order of entries & appending new ones at the end")
    
    args = parser.parse_args()
    # Ensure the output folder exists
    output_folder = args.output_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    existing_entries_log_file = os.path.join(args.output_folder, 'existing_entries_log_file.txt')
    existing_entries = parse_xml(args.existing_entries_file,existing_entries_log_file)
    new_entries_log_file = os.path.join(args.output_folder, 'new_entries_log_file.txt')
    existing_new_entries = parse_xml(args.new_entries_file,new_entries_log_file)
    generate_output(existing_entries, existing_new_entries, args.output_folder, args.sort_by, args.preserve_original_order)

if __name__ == "__main__":
    main()
