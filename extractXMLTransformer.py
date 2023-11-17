from lxml import etree
import argparse
import sys
import os

class XMLTransformer:
    def __init__(self, input_file, output_folder, debug=False):
        self.input_file = input_file
        # Construct the output file name by replacing the .xml extension with .csv
        output_file_name = os.path.splitext(os.path.basename(input_file))[0] + '.csv'
        self.output_file = os.path.join(output_folder, output_file_name)
        self.debug = debug
        self.extracted_strings = [] # Initialize a list to hold the extracted strings


    def normalize_xml(self, xml_content):
        # Define the replacements as a list of tuples
        replacements = [
            ('</csvBeginTypes>', ''),
            ('<csvBeginTypes handler="com.ptc.core.lwc.server.TypeDefinitionLoader.beginProcessTypes"/>', '<csvBeginTypes handler="com.ptc.core.lwc.server.TypeDefinitionLoader.beginProcessTypes">'),
            ('</csvBeginTypeDefView>', ''),
            ('</csvBeginLayoutDefView>', ''),
            ('</csvBeginGroupDefView>', ''),
            ('</csvBeginGroupMemberView>', ''),
            ('</csvBeginAttributeDefView>', ''),
            ('</csvBeginConstraintDefView>', ''),
            ('</csvBeginEnumDefView>', ''),
            ('</csvBeginEnumMemberView>', ''),
            ('<csvEndEnumMemberView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessEnumMembership"/>', '</csvBeginEnumMemberView>'),
            ('<csvEndEnumMemberView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumMembership"/>', '</csvBeginEnumMemberView>'),
            ('<csvEndEnumDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessEnumerationDefinition"/>', '</csvBeginEnumDefView>'),
            ('<csvEndEnumDefView handler="com.ptc.core.lwc.server.BaseDefinitionLoader.endProcessEnumerationDefinition"/>', '</csvBeginEnumDefView>'),
            ('<csvEndConstraintDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessConstraintDefinition"/>', '</csvBeginConstraintDefView>'),
            ('<csvEndAttributeDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessAttributeDefinition"/>', '</csvBeginAttributeDefView>'),
            ('<csvEndGroupMemberView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessGroupMembership"/>', '</csvBeginGroupMemberView>'),
            ('<csvEndGroupDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessGroupDefinition"/>', '</csvBeginGroupDefView>'),
            ('<csvEndLayoutDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessLayoutDefinition"/>', '</csvBeginLayoutDefView>'),
            ('<csvEndTypeDefView handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessTypeDefinition"/>', '</csvBeginTypeDefView>'),
            ('<csvEndTypes handler="com.ptc.core.lwc.server.TypeDefinitionLoader.endProcessTypes"/>', '</csvBeginTypes>'),
        ]

        # Perform the replacements in order
        for old, new in replacements:
            xml_content = xml_content.replace(old, new)

        return xml_content

    def save_debug_output(self, content):
        debug_output_file =  os.path.splitext(self.output_file)[0] + '_normalized.xml'
        with open(debug_output_file, 'w') as f:
            f.write(content)
        print(f"Debug output saved to {debug_output_file}")

    def transform(self):
        # Read the XML file content
        with open(self.input_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        # Normalize the XML content
        normalized_xml_content = self.normalize_xml(xml_content)
        # Save the normalized content for debugging
        if self.debug:
            self.save_debug_output(normalized_xml_content)
        # Parse the normalized XML content
        root = etree.fromstring(normalized_xml_content.encode('utf-8'))
        begin_types = root.xpath(".//csvBeginTypes")
        classifications = False
        types = False
        for element in begin_types:
            if element.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCTYPE']"):
                types = True
                break
            elif element.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCSTRUCT']"):
                classifications = True
                break
        if types:
            print('Processing Types structure: ' + self.input_file)
            self.extract_data_Types(root)
        elif classifications:
            print('Processing Classification structure: ' + self.input_file)
            self.extract_data_Classification(root)
        elif root.xpath(".//csvBeginEnumMemberView"):
            print('Processing EnumDefView structure: ' + self.input_file)
            self.extract_data_Enums(root)
        else:
            print('Different or unknown XML structure detected.')
            # Placeholder for future functionality

        # Write the extracted strings to the output file
        self.write_output(self.output_file)

    def extract_data_Enums(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()
        for enum_def_view in root.xpath(".//csvBeginEnumDefView"):
            # Extract the displayName value
            display = enum_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")
            self.extracted_strings.append(display[0])
            # Extract the name value
            # name = enum_def_view.findtext('./csvname') or ''
            name = enum_def_view.xpath("./csvname/text()")[0] or ''
            self.extracted_strings.append(name)
            # Prepare the header line for the CSV content: concatenation of name and display name with | to split them
            header_line = "name~displayName"
            self.extracted_strings.append(header_line)
            # Extract information for each 'csvBeginEnumMemberView'
            for enum_member in enum_def_view.xpath(".//csvBeginEnumMemberView"):
                member_info = self.extract_data_Enums_member_info(enum_member)
                if member_info:
                    self.extracted_strings.append(member_info)
        return self.extracted_strings

    def extract_data_Enums_member_info(self, enum_member):
        member_name = enum_member.xpath("./csvname/text()")[0]
        display_name = enum_member.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")
        display_name = display_name[0] if display_name else '' 
        selectable = enum_member.xpath("./csvPropertyValue[csvname='selectable'][1]/csvvalue/text()")
        if not display_name or not selectable or selectable[0].lower() == 'false':
            return None
        
        return f"{member_name}~{display_name}"

    def extract_data_Types(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()
        # Prepare the header line for the CSV content
        header_line = "name~display~required~class~iba~type~length~unit~single~upperCase~regularExpr~defaultValue~list~enumMembers"
        self.extracted_strings.append(header_line)

        # Iterate over each csvBeginTypeDefView element
        for type_def_view in root.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCTYPE']"):
            instantiable = type_def_view.xpath("./csvPropertyValue[csvname='instantiable']/csvvalue/text()")
            if instantiable and instantiable[0].lower() == 'true':
                # Iterate over each csvBeginAttributeDefView element within csvBeginTypeDefView
                for attr_def_view in type_def_view.xpath("./csvBeginAttributeDefView"):
                    name = display = iba = class_value = datatype = length = unit = defaultValue = list_value = enum_members = ''
                    required = single = upperCase = 'No'
                    regularExpr = ''

                    # Process for name, class, defaultValue, dataType and unit
                    iba = attr_def_view.findtext('./csvIBA') or ''
                    name = attr_def_view.findtext('./csvname') or ''
                    display = attr_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")
                    display = display[0] if display else ''                    

                    class_value = attr_def_view.findtext('./csvattDefClass') or ''
                    class_value = class_value.replace('com.ptc.core.lwc.server.', '')

                    defaultValue = attr_def_view.findtext('./csvdefaults') or ''
                    defaultValue = defaultValue.replace('DATA|java.lang.String|', '')
                    defaultValue = defaultValue.replace('DATA|java.lang.long|', '')
                    defaultValue = defaultValue.replace('DATA|java.lang.Boolean|', '')

                    datatype = attr_def_view.findtext('./csvdatatype') or ''
                    datatype = datatype.replace('java.lang.', '')
                    datatype = datatype.replace('java.sql.', '')
                    datatype = datatype.replace('wt.units.', '')

                    unit = attr_def_view.findtext('./csvQoM') or ''

                    # Process constraints within the attribute
                    for constraint_def_view in attr_def_view.xpath("./csvBeginConstraintDefView"):
                        rule_classname = constraint_def_view.findtext('csvruleClassname')
                        if 'ValueRequiredConstraint' in rule_classname:
                            required = 'Yes'
                        if 'StringLengthConstraint' in rule_classname:
                            length = constraint_def_view.findtext('csvruleData') or ''
                            length = length.replace('DATA|com.ptc.core.meta.common.AnalogSet|[DATA|java.lang.Long|', '')
                            length = length.replace(r' \, DATA|java.lang.Long|', '-')
                            length = length.replace(']', '')
                        if 'RegularExpressionConstraint' in rule_classname:
                            regularExpr = constraint_def_view.findtext('csvruleData') or ''
                            regularExpr = regularExpr.replace('DATA|com.ptc.core.meta.common.RegularExpressionSet|DATA|java.lang.Boolean|false , DATA|java.lang.String|', '')
                        if 'SingleValuedConstraint' in rule_classname:
                            single = 'Yes'
                        if 'UpperCaseConstraint' in rule_classname:
                            upperCase = 'Yes'
                        if 'DiscreteSetConstraint' in rule_classname:
                            list_value = constraint_def_view.findtext('csvdefQualifier')
                            if not list_value: # If csvdefQualifier value is empty
                                # Try to get csvname value
                                next_enum_def = constraint_def_view.xpath("./csvBeginEnumDefView[1]/csvname/text()")
                                if next_enum_def and next_enum_def[0]:
                                    list_value = next_enum_def[0]
                                else:
                                    # Fallback to csvmaster and call extract_data_Types_member_names
                                    csvmaster_value = constraint_def_view.xpath("./csvBeginEnumDefView[1]/csvmaster/text()")
                                    if csvmaster_value:
                                        list_value = csvmaster_value[0]
                                        enum_members = self.extract_data_Types_member_names(constraint_def_view)

                    # Append the extracted data as a new line
                    self.extracted_strings.append(f"{name}~{display}~{required}~{class_value}~{iba}~{datatype}~{length}~{unit}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}")
            # else:
            #     print('Type non instantiable for : '+self.output_file+' - File not created !')

        # remove if only header to prevent csv file with empty value
        if len(self.extracted_strings) == 1:
            self.extracted_strings.clear()
        return self.extracted_strings

    def extract_data_Types_member_names(self, constraint_def_view):
        member_names = []
        # Start from the constraint definition view and iterate through following elements
        for enum_def_view in constraint_def_view.xpath("./csvBeginEnumDefView[1]"):
            for enum_member in enum_def_view.xpath(".//csvBeginEnumMemberView"):
                member_name = enum_member.xpath("./csvname/text()")[0]
                selectable = enum_member.xpath("./csvPropertyValue[csvname='selectable'][1]/csvvalue/text()")
                if member_name and selectable[0].lower() == 'true':
                    member_names.append(member_name)
        return '|'.join(member_names)

    def extract_data_Classification(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()

        # Prepare the header line for the CSV content
        header_line = "name~display~required~class~iba~type~length~unit~single~upperCase~regularExpr~defaultValue~list~enumMembers"
        self.extracted_strings.append(header_line)

        # Iterate over each csvBeginTypeDefView element
        for type_def_view in root.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCSTRUCT']"):
            instantiable = type_def_view.xpath("./csvPropertyValue[csvname='instantiable']/csvvalue/text()")
            if instantiable and instantiable[0].lower() == 'true':
                # Iterate over each csvBeginAttributeDefView element within csvBeginTypeDefView
                for attr_def_view in type_def_view.xpath("./csvBeginAttributeDefView"):
                    name = display = iba = class_value = datatype = length = unit = defaultValue = list_value = enum_members = ''
                    required = single = upperCase = 'No'
                    regularExpr = ''

                    # Process for name, class, defaultValue, dataType and unit
                    iba = attr_def_view.findtext('./csvIBA') or ''
                    name = attr_def_view.findtext('./csvname') or ''
                    display = attr_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")
                    display = display[0] if display else ''                    

                    class_value = attr_def_view.findtext('./csvattDefClass') or ''
                    class_value = class_value.replace('com.ptc.core.lwc.server.', '')

                    defaultValue = attr_def_view.findtext('./csvdefaults') or ''
                    defaultValue = defaultValue.replace('DATA|java.lang.String|', '')
                    defaultValue = defaultValue.replace('DATA|java.lang.long|', '')
                    defaultValue = defaultValue.replace('DATA|java.lang.Boolean|', '')

                    datatype = attr_def_view.findtext('./csvdatatype') or ''
                    datatype = datatype.replace('java.lang.', '')
                    datatype = datatype.replace('java.sql.', '')
                    datatype = datatype.replace('wt.units.', '')

                    unit = attr_def_view.findtext('./csvQoM') or ''

                    # Process constraints within the attribute
                    for constraint_def_view in attr_def_view.xpath("./csvBeginConstraintDefView"):
                        rule_classname = constraint_def_view.findtext('csvruleClassname')
                        if 'ValueRequiredConstraint' in rule_classname:
                            required = 'Yes'
                        if 'StringLengthConstraint' in rule_classname:
                            length = constraint_def_view.findtext('csvruleData') or ''
                            length = length.replace('DATA|com.ptc.core.meta.common.AnalogSet|[DATA|java.lang.Long|', '')
                            length = length.replace(r' \, DATA|java.lang.Long|', '-')
                            length = length.replace(']', '')
                        if 'RegularExpressionConstraint' in rule_classname:
                            regularExpr = constraint_def_view.findtext('csvruleData') or ''
                            regularExpr = regularExpr.replace('DATA|com.ptc.core.meta.common.RegularExpressionSet|DATA|java.lang.Boolean|false , DATA|java.lang.String|', '')
                        if 'SingleValuedConstraint' in rule_classname:
                            single = 'Yes'
                        if 'UpperCaseConstraint' in rule_classname:
                            upperCase = 'Yes'
                        if 'DiscreteSetConstraint' in rule_classname:
                            list_value = constraint_def_view.findtext('csvdefQualifier')
                            if not list_value: # If csvdefQualifier value is empty
                                # Try to get csvname value
                                next_enum_def = constraint_def_view.xpath("./csvBeginEnumDefView[1]/csvname/text()")
                                if next_enum_def and next_enum_def[0]:
                                    list_value = next_enum_def[0]
                                else:
                                    # Fallback to csvmaster and call extract_data_Types_member_names
                                    csvmaster_value = constraint_def_view.xpath("./csvBeginEnumDefView[1]/csvmaster/text()")
                                    if csvmaster_value:
                                        list_value = csvmaster_value[0]
                                        enum_members = self.extract_data_Types_member_names(constraint_def_view)

                    # Append the extracted data as a new line
                    self.extracted_strings.append(f"{name}~{display}~{required}~{class_value}~{iba}~{datatype}~{length}~{unit}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}")
            # else:
            #     print('Type non instantiable for : '+self.output_file+' - File not created !')

        # remove if only header to prevent csv file with empty value
        if len(self.extracted_strings) == 1:
            self.extracted_strings.clear()
        return self.extracted_strings

    def write_output(self,output_csv_file):
        if self.extracted_strings:
            # with open(self.output_csv_file, 'w', encoding='utf-8') as f:
            with open(output_csv_file, 'w') as f:
                for string in self.extracted_strings:
                    f.write(string + '\n')
            print(f"CSV File saved to {output_csv_file}")
        else:
            print('CSV File not created, no data found !')

def run():
    parser = argparse.ArgumentParser(description="Transform an XML file to a text file based on specific rules.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input XML file path")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output folder")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode to output the normalized XML file")
    args = parser.parse_args()

    try:
        transformer = XMLTransformer(args.input, args.output, args.debug)
        transformer.transform()
    except Exception as e:
        print(f"An error occurred while transforming {args.input}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # XMLTransformer.run()
    run()
