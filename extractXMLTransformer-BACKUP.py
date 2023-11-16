from lxml import etree
import argparse
import sys

class XMLTransformer:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.extracted_strings = [] # Initialize a list to hold the extracted strings

    def transform(self):
        # Parse the XML file
        tree = etree.parse(self.input_file)
        root = tree.getroot()

        if root.xpath(".//csvBeginTypes"):
            print('Processing Types structure: ' + self.input_file)
            self.extract_data_Types(root)
        elif root.xpath(".//csvBeginEnumMemberView"):
            print('Processing EnumDefView structure: ' + self.input_file)
            self.extract_data_EnumDefView(root)
        else:
            print('Different or unknown XML structure detected.')
            # Placeholder for future functionality

        # Write the extracted strings to the output file
        self.write_output()

    def extract_data_EnumDefView(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()

        # Extract the displayName value
        # display_name_value = root.xpath(".//csvPropertyValue[csvname='displayName']/csvvalue/text()")[0]
        # self.extracted_strings.append(display_name_value)

        # Extract the name value
        # enum_def_name = root.xpath(".//csvBeginEnumDefView/csvname/text()")[0]
        # self.extracted_strings.append(enum_def_name)
        
        # Prepare the header line for the CSV content: concatenation of name and display name with | to split them
        header_line = "name|displayName"
        self.extracted_strings.append(header_line)

        # Rule 3: Extract information for each 'csvBeginEnumMemberView'
        for enum_member in root.xpath(".//csvBeginEnumMemberView"):
            member_info = self.extract_member_info(enum_member)
            if member_info:
                self.extracted_strings.append(member_info)

        return self.extracted_strings

    def extract_data_Types(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()

        # Prepare the header line for the CSV content
        header_line = "name~display~required~class~iba~type~length~unit~single~defaultValue~list~enumMembers"
        self.extracted_strings.append(header_line)

        # Iterate over each csvBeginTypeDefView element
        for type_def_view in root.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCTYPE']"):
            instantiable = type_def_view.xpath("following-sibling::csvPropertyValue[csvname='instantiable'][1]/csvvalue/text()")
            if instantiable and instantiable[0].lower() == 'true':
                # Iterate over each csvBeginAttributeDefView element within csvBeginTypeDefView
                for attr_def_view in root.xpath(".//csvBeginAttributeDefView"):
                    name = display = iba = class_value = datatype = length = unit = defaultValue = list_value = enum_members = ''
                    required = single = 'No'

                    # Process for name, class, and defaultValue
                    iba = attr_def_view.findtext('csvIBA') or ''
                    name = attr_def_view.findtext('csvname') or ''
                    class_value = attr_def_view.findtext('csvattDefClass') or ''
                    defaultValue = attr_def_view.findtext('csvdefaults') or ''

                    # Process for constraints within the attribute
                    for el in attr_def_view.xpath("following-sibling::*"):
                        if el.tag == 'csvEndAttributeDefView':
                            break
                        if el.tag == 'csvBeginConstraintDefView':
                            rule_classname = el.findtext('csvruleClassname')
                            if 'ValueRequiredConstraint' in rule_classname:
                                required = 'Yes'
                            if 'StringLengthConstraint' in rule_classname:
                                length = el.findtext('csvruleData') or ''
                            if 'SingleValuedConstraint' in rule_classname:
                                single = 'Yes'
                            if 'DiscreteSetConstraint' in rule_classname:
                                list_value = el.findtext('csvdefQualifier')
                                if not list_value:  # If csvdefQualifier value is empty
                                    # Find the next csvBeginEnumDefView with csvname starting with 'GlobalEnum'
                                    # next_enum_def = el.xpath("following-sibling::csvBeginEnumDefView[starts-with(csvname, 'GlobalEnum')][1]/csvname/text()") # el.xpath("following::csvBeginEnumDefView[starts-with(csvname, 'GlobalEnum')][1]/csvname/text()")
                                    next_enum_def = el.xpath("following-sibling::csvBeginEnumDefView[1]/csvname/text()")
                                    list_value = next_enum_def[0] if next_enum_def else ''

                                # Check for csvBeginEnumDefView followed by csvBeginEnumMemberView
                                # for enum_def_view in attr_def_view.xpath("following-sibling::csvBeginEnumDefView"):
                                for enum_def_view in el.xpath("following-sibling::csvBeginEnumDefView"):
                                    member_names = []
                                    # for sibling in enum_def_view.itersiblings():
                                    for sibling in enum_def_view.xpath("following-sibling::*"):
                                        if sibling.tag == 'csvEndEnumDefView':
                                            break
                                        if sibling.tag == 'csvBeginEnumMemberView':
                                            selectable = sibling.xpath("following-sibling::csvPropertyValue[csvname='selectable'][1]/csvvalue/text()")
                                            if selectable and selectable[0] == 'true':
                                                member_name = sibling.findtext('csvname')
                                                if member_name:
                                                    member_names.append(member_name)
                                    if member_names:
                                        enum_members = ', '.join(member_names)
                                        #break  # Process only the first relevant csvBeginEnumDefView

                    # Process for datatype and unit
                    datatype = attr_def_view.findtext('csvdatatype') or ''
                    unit = attr_def_view.findtext('csvQoM') or ''

                    # Append the extracted data as a new line
                    self.extracted_strings.append(f"{name}~{display}~{required}~{class_value}~{iba}~{datatype}~{length}~{unit}~{single}~{defaultValue}~{list_value}~{enum_members}")
            else:
                print('Type non instantiable for : '+self.output_file+' - File not created !')

        # remove if only header to prevent csv file with empty value
        if len(self.extracted_strings) == 1:
            self.extracted_strings.clear()
        return self.extracted_strings

    def extract_member_info(self, enum_member):
        member_name = enum_member.xpath("./csvname/text()")[0]
        display_name = enum_member.xpath("following-sibling::csvPropertyValue[csvname='displayName'][1]/csvvalue/text()")
        selectable = enum_member.xpath("following-sibling::csvPropertyValue[csvname='selectable'][1]/csvvalue/text()")
        
        if not display_name or not selectable or selectable[0].lower() == 'false':
            return None
        
        return f"{member_name}|{display_name[0]}"

    def write_output(self):
        if self.extracted_strings:
            with open(self.output_file, 'w') as f:
                for string in self.extracted_strings:
                    f.write(string + '\n')
        else:
            print('No data found for : '+self.output_file+' - File not created !')

def run():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Transform an XML file to a text file based on specific rules.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input XML file path")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output text file path")
    args = parser.parse_args()

    try:
        transformer = XMLTransformer(args.input, args.output)
        transformer.transform()
        print(f"Transformation complete. Output saved to {args.output}")
    except Exception as e:
        print(f"An error occurred while transforming {args.input}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    XMLTransformer.run()
