import csv
import xml.etree.ElementTree as ET
import sys

def read_csv_tuples(csv_file_path):
    new_tuples = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Adjust these keys according to your CSV column names.
            new_tuples.append((row['internalName'], row['displayName'], row['selectable'], row.get('sort_order', '0')))
    # Sort tuples by internalName to ensure correct order upon insertion
    new_tuples.sort(key=lambda x: x[0])
    return new_tuples

def find_insertion_index(root, new_tuple_name):
    """Find the correct position to insert the new enumerated value based on its name."""
    last_index = None
    for index, elem in enumerate(root.findall('.//csvBeginEnumMemberView')):
        name = elem.find('csvname').text
        if name > new_tuple_name:
            return index
        last_index = index
    return last_index + 1 if last_index is not None else 0

def insert_enumerated_value(root, tuple, index):
    name, displayName, selectable, sort_order = tuple
    # Create and insert csvBeginEnumMemberView
    enum_begin = ET.Element('csvBeginEnumMemberView', {'handler': "com.ptc.core.lwc.server.BaseDefinitionLoader.beginProcessEnumMembership"})
    ET.SubElement(enum_begin, 'csvname').text = name
    root.insert(index, enum_begin)

    # Increment index for subsequent inserts
    index += 1

    # Insert properties (displayName, selectable, sort_order)
    for prop_name, value in [('displayName', displayName), ('selectable', selectable), ('sort_order', sort_order)]:
        prop = ET.Element('csvPropertyValue', {'handler': "com.ptc.core.lwc.server.BaseDefinitionLoader.processEnumEntryPropertyValue"})
        ET.SubElement(prop, 'csvname').text = prop_name
        ET.SubElement(prop, 'csvvalue').text = value
        root.insert(index, prop)
        index += 1

    # Insert csvEndEnumMemberView
    enum_end = ET.Element('csvEndEnumMemberView', {'handler': "com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumMembership"})
    root.insert(index, enum_end)

def update_xml_file(xml_file_path, csv_file_path, output_xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    new_tuples = read_csv_tuples(csv_file_path)
    
    for tuple in new_tuples:
        index = find_insertion_index(root, tuple[0])
        insert_enumerated_value(root, tuple, index)

    tree.write(output_xml_file_path, encoding='utf-8', xml_declaration=True)

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py path_to_original_xml_file path_to_csv_file path_to_output_xml_file")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    csv_file_path = sys.argv[2]
    output_xml_file_path = sys.argv[3]
    update_xml_file(xml_file_path, csv_file_path, output_xml_file_path)

if __name__ == "__main__":
    main()
