import csv
import xml.etree.ElementTree as ET
import sys

def read_csv_tuples(csv_file_path):
    """
    Reads new tuples from a CSV file.
    
    Parameters:
        csv_file_path (str): The path to the CSV file containing new tuples.
    
    Returns:
        list of tuples: A list of tuples with new values to be inserted into the XML.
    """
    new_tuples = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Assuming columns are named 'internalName', 'displayName', 'selectable'
            new_tuples.append((row['internalName'], row['displayName'], row['selectable']))
    return new_tuples

def get_enumerated_values(root):
    """
    Extracts existing enumerated values and their details from the XML root.
    """
    enumerated_values = []
    for enum_member in root.findall(".//csvBeginEnumMemberView"):
        internal_name = enum_member.find(".//csvname").text
        display_name_element = enum_member.find(".//csvPropertyValue[@csvname='displayName']/csvvalue")
        selectable_element = enum_member.find(".//csvPropertyValue[@csvname='selectable']/csvvalue")
        
        # Handle cases where elements might be missing
        display_name = display_name_element.text if display_name_element is not None else ""
        selectable = selectable_element.text if selectable_element is not None else ""
        
        handler = enum_member.get('handler')
        enumerated_values.append({
            'internalName': internal_name,
            'displayName': display_name,
            'selectable': selectable,
            'handler': handler
        })
    return enumerated_values

def rebuild_enumerated_values_section(root, all_values):
    """
    Rebuilds the section of the XML containing enumerated values. Each enumerated value
    and its properties are encapsulated between csvBeginEnumMemberView and csvEndEnumMemberView tags.
    """
    # Directly find the parent element of csvBeginEnumDefView to insert the new elements
    enum_def_section = root.find('.//csvBeginEnumDefView/..')
    if enum_def_section is None:
        print("Could not locate the enumeration definition section.")
        return

    # Find the position of csvBeginEnumDefView within its parent to know where to start inserting
    enum_def_view = root.find('.//csvBeginEnumDefView')
    start_inserting_at = list(enum_def_section).index(enum_def_view) + 1 if enum_def_view else 0

    # Remove existing enumerated values
    for elem in enum_def_section.findall(".//csvBeginEnumMemberView") + enum_def_section.findall(".//csvEndEnumMemberView"):
        enum_def_section.remove(elem)

    # Sort all_values by internal name to determine new order
    sorted_values = sorted(all_values, key=lambda x: x['internalName'])

    # Insert new enumerated values
    for value in sorted_values:
        # Begin enumerated value definition
        enum_member_view = ET.Element('csvBeginEnumMemberView', {'handler': value['handler']})
        ET.SubElement(enum_member_view, 'csvname').text = value['internalName']
        
        # Add displayName property
        dp_property = ET.SubElement(enum_member_view, 'csvPropertyValue', {'handler': 'com.ptc.core.lwc.server.BaseDefinitionLoader.processEnumEntryPropertyValue'})
        ET.SubElement(dp_property, 'csvname').text = 'displayName'
        ET.SubElement(dp_property, 'csvvalue').text = value['displayName']
        
        # Add selectable property
        sel_property = ET.SubElement(enum_member_view, 'csvPropertyValue', {'handler': 'com.ptc.core.lwc.server.BaseDefinitionLoader.processEnumEntryPropertyValue'})
        ET.SubElement(sel_property, 'csvname').text = 'selectable'
        ET.SubElement(sel_property, 'csvvalue').text = value['selectable']

        # Insert the begin tag and properties into the parent
        enum_def_section.insert(start_inserting_at, enum_member_view)
        start_inserting_at += 1

        # Insert the end tag
        enum_member_end = ET.Element('csvEndEnumMemberView', {'handler': value['handler']})
        enum_def_section.insert(start_inserting_at, enum_member_end)
        start_inserting_at += 1


def insert_and_reorder_xml(xml_file_path, new_tuples):
    """
    Inserts new tuples into the XML and reorders all enumerated values based on their internal names.
    Updates the 'sort_order' for each value accordingly.
    
    Parameters:
        xml_file_path (str): The path to the source XML file.
        new_tuples (list of tuples): New tuples to insert.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract existing enumerated values
    existing_values = get_enumerated_values(root)

    # Convert new tuples to dict format and append to existing values
    all_values = existing_values + [{'internalName': nt[0], 'displayName': nt[1], 'selectable': nt[2], 'handler': 'specify handler'} for nt in new_tuples]

    # Rebuild the enumerated values section with updated and new values
    rebuild_enumerated_values_section(root, all_values)

    # Save the updated XML to a new file
    tree.write('updated_formats.xml', encoding='utf-8', xml_declaration=True)

def main():
    """
    Main function to process the XML and CSV files.
    """
    if len(sys.argv) < 3:
        print("Usage: python script.py path_to_your_original_xml.xml path_to_your_new_values.csv")
        sys.exit(1)

    xml_file_path = sys.argv[1]
    csv_file_path = sys.argv[2]
    new_tuples = read_csv_tuples(csv_file_path)
    insert_and_reorder_xml(xml_file_path, new_tuples)

if __name__ == "__main__":
    main()
