from lxml import etree
import argparse
import os

class XMLTransformer:
    def __init__(self, input_file, output_folder, debug=False):
        print('   -------------------------------BEGIN TRANSFORM--------------------------------------')
        self.input_file = input_file
        # Construct the output file name by replacing the .xml extension with .csv
        output_file_name = os.path.splitext(os.path.basename(input_file))[0] + '.csv'
        self.output_file = os.path.join(output_folder, output_file_name)
        self.debug = debug
        self.extracted_strings = [] # Initialize a list to hold the extracted strings

    def __del__(self):
        print('   -------------------------------END   TRANSFORM--------------------------------------')

    def normalize_xml(self, xml_content):
        # Define the replacements as a list of tuples to be executed in same order
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
        print(f"   Debug output saved to {debug_output_file}")

    def transform(self):
        try:
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
                print('   Processing Types structure: ' + self.input_file)
                self.extract_data_Types(root)
            elif classifications:
                print('   Processing Classification structure: ' + self.input_file)
                self.extract_data_Classification(root)
            elif root.xpath(".//csvBeginEnumMemberView"):
                print('   Processing Global Enumeration structure: ' + self.input_file)
                self.extract_data_Enums(root)
            else:
                print('   Unknown XML structure detected: ' + self.input_file)
                # Placeholder for future functionality

            # Write the extracted strings to the output file
            self.write_output(self.output_file)
        except Exception as e:
            message = f"******************  Transform xml file failed: ******************"
            length = len(message)
            stars = '*' * length
            marks = '!' * length
            print("   "+stars)
            print("   "+marks)
            print("   "+message)
            exception_type = type(e).__name__
            print(f"   {exception_type}: {e}")
            print("   "+marks)
            print("   "+stars)

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
            # Prepare the header line for the CSV content
            header_line = "name~displayName"
            self.extracted_strings.append(header_line)
            # Extract information for each 'csvBeginEnumMemberView'
            for enum_member in enum_def_view.xpath(".//csvBeginEnumMemberView"):
                member_info = self.extract_data_Enums_member_info(enum_member)
                if member_info:
                    self.extracted_strings.append(member_info)
            # Add an empty row after processing each enum_def_view
            self.extracted_strings.append('<EMPTY_ROW>') 
                   
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
        header_line = "name~display~iba~required~type~unit~length~single~upperCase~regularExpr~defaultValue~legalValues~EnumeratedValues"

        # Iterate over each csvBeginTypeDefView element
        for type_def_view in root.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCTYPE']"):

            # Extract the type name
            typeName = type_def_view.xpath("./csvname/text()")[0] or ''
            if typeName:
                self.extracted_strings.append(typeName)
            else:
                self.extracted_strings.append('ERROR_EXTRACTING_TYPE_NAME')
            # Extract the type display name
            typeDisplayName = type_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")[0] or ''
            if typeDisplayName:
                self.extracted_strings.append(typeDisplayName)
            else:
                self.extracted_strings.append('ERROR_EXTRACTING_TYPE_DISPLAY_NAME')

            self.extracted_strings.append(header_line)
            instantiable = type_def_view.xpath("./csvPropertyValue[csvname='instantiable']/csvvalue/text()")
            if instantiable and instantiable[0].lower() == 'true':
                # Iterate over each csvBeginAttributeDefView element within csvBeginTypeDefView
                for attr_def_view in type_def_view.xpath("./csvBeginAttributeDefView"):
                    self.extract_attribute_definitions(attr_def_view, '', '', 0, instantiable, '', 'Types')

            # Add an empty row after processing each type_def_view
            self.extracted_strings.append('<EMPTY_ROW>') 

        # Remove all content if no attributes found to prevent any csv file with empty value
        if len(self.extracted_strings) == 4 and self.extracted_strings[3]== '<EMPTY_ROW>' :
            self.extracted_strings.clear()

        return self.extracted_strings

    def extract_data_Classification(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()

        # Prepare the header line for the CSV content
        header_line = "depth~type~parentType~instantiable~displayType~name~display~iba~required~type~unit~length~single~upperCase~regularExpr~defaultValue~legalValues~EnumeratedValues"
        self.extracted_strings.append(header_line)

        # keep track of typeObject and its depth
        type_depth_map = {}

        # Iterate over each csvBeginTypeDefView element
        for type_def_view in root.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCSTRUCT']"):
            typeObject = parentType = displayType = ''
            instantiable = 'No'
            name = display = iba = datatype = length = unit = defaultValue = list_value = enum_members = regularExpr = ''
            required = single = upperCase = instantiable = ''

            typeObject = type_def_view.findtext('./csvname') or ''
            parentType = type_def_view.findtext('./csvtypeParent') or ''
            instantiable = type_def_view.xpath("./csvPropertyValue[csvname='instantiable']/csvvalue/text()") or ''
            if instantiable and instantiable[0].lower() == 'true':
                instantiable = 'Yes'
            else:
                instantiable = 'No'
            displayType = type_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")
            displayType = displayType[0] if displayType else ''

            # Calculate depth
            depth = 0
            current_parent = parentType
            while current_parent:
                depth += 1
                current_parent = type_depth_map.get(current_parent, None)
            type_depth_map[typeObject] = parentType  # Map current type to its parent


            # Append the extracted type as a new line
            self.extracted_strings.append(f"{depth}~{typeObject}~{parentType}~{instantiable}~{displayType}~{name}~{display}~{iba}~{required}~{datatype}~{unit}~{length}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}")

            for attr_def_view in type_def_view.xpath("./csvBeginAttributeDefView"):
                self.extract_attribute_definitions(attr_def_view, typeObject, parentType, depth, instantiable, displayType, 'Classification')
        # else:
        #     print('Type non instantiable for : '+self.output_file+' - File not created !')

        # remove if only header to prevent csv file with empty value
        if len(self.extracted_strings) == 1:
            self.extracted_strings.clear()
        return self.extracted_strings

    def extract_attribute_definitions(self, attr_def_view, typeObject, parentType, depth, instantiable, displayType, mode):
            name = display = class_value = datatype = length = unit = defaultValue = list_value = enum_members = regularExpr = ''
            required = single = upperCase = iba = 'No'
            
            # Process for name, class, defaultValue, dataType and unit
            if attr_def_view.findtext('./csvIBA'):
                iba = 'Yes'
            name = attr_def_view.findtext('./csvname') or ''

            # Process for required, single, upperCase, length, unit

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
            datatype = datatype.replace('com.ptc.core.meta.common.', '')

            unit = attr_def_view.findtext('./csvQoM') or ''
            # Add displayed unit - maybe be different from database units - TBC
            unit = unit.replace('Electrical Capacitance', 'Electrical Capacitance (F)')
            unit = unit.replace('Electrical Current', 'Electrical Current (A)')
            unit = unit.replace('Mass', 'Mass (Kg)')
            unit = unit.replace('Temperature', 'Temperature (degC)')
            unit = unit.replace('Luminous Flux', 'Luminous Flux (lm)')
            unit = unit.replace('Electrical Potential', 'Electrical Potential (V)')
            unit = unit.replace('Frequency', 'Frequency (Hz)')
            unit = unit.replace('Electrical Inductance', 'Electrical Inductance (H)')
            unit = unit.replace('Luminous Intensity', 'Luminous Intensity (cd)')
            unit = unit.replace('Pressure', 'Pressure (kPa)')
            unit = unit.replace('Length', 'Length (mm)')
            unit = unit.replace('Power', 'Power (W)')
            unit = unit.replace('Electrical Resistance', 'Electrical Resistance (ohm)')
            unit = unit.replace('Area', 'Area (m**2)')
            unit = unit.replace('Time', 'Time (s)')

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
                    # If csvdefQualifier value is not empty: this is specific to Classification rule data
                    list_value = constraint_def_view.findtext('csvdefQualifier') or ''
                    if list_value:
                        # classification node value that is set as a constraint
                        # list_value = list_value + ': ' + (constraint_def_view.findtext('csvruleData') or '')
                        list_value = constraint_def_view.findtext('csvruleData') or ''
                        list_value = list_value.replace('DATA|com.ptc.core.meta.common.DiscreteSet|DATA|java.lang.Boolean|false , DATA|java.lang.String|com.ptc.core.lwc.common.dynamicEnum.provider.ClassificationEnumerationInfoProvider|ns=com.ptc.csm.default_clf_namespace:nn=', '')
                    else:
                        # Try to get csvname value
                        enum_def = constraint_def_view.xpath("./csvBeginEnumDefView[1]/csvname/text()")
                        if enum_def and enum_def[0]:
                            enum_members = enum_def[0] # Name of Global Enum without values being overriden
                        else:
                            # Fallback to csvruleData for Legal Value List
                            list_value = constraint_def_view.findtext('csvruleData') or ''
                            if list_value:
                                #list_value = 'LVL: ' + list_value
                                list_value = list_value.replace('DATA|com.ptc.core.meta.common.DiscreteSet|DATA|java.lang.Boolean|false , ', '')
                                list_value = list_value.replace('DATA|java.lang.String|', '')
                                list_value = list_value.replace('DATA|java.lang.Long|', '')
                                list_value = list_value.replace(' , ', '|')
                            else:
                                # Fallback to csvmaster for overriden Global Enums
                                csvmaster_value = constraint_def_view.xpath("./csvBeginEnumDefView[1]/csvmaster/text()")
                                if csvmaster_value:
                                    enum_members = csvmaster_value[0] # Name of Global Enum with values being overriden
                                    enum_members = enum_members + ': ' + self.extract_data_Types_member_names(constraint_def_view) # List of values with selectable=yes

            # Replace length with default value for String if empty (information not available in XML)
            if length == '' and datatype == 'String':
                length = '500'
            elif length.startswith('0-'):
                length = length.replace('0-', '', 1) # Update format of value 

            # Append the extracted attributes as a new line
            if mode == 'Classification':
                self.extracted_strings.append(f"{depth}~{typeObject}~{parentType}~{instantiable}~{displayType}~{name}~{display}~{iba}~{required}~{datatype}~{unit}~{length}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}")
            elif mode == 'Types':
                    self.extracted_strings.append(f"{name}~{display}~{iba}~{required}~{datatype}~{unit}~{length}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}")

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

    def write_output(self,output_csv_file):
        if self.extracted_strings:
            # with open(self.output_csv_file, 'w', encoding='utf-8') as f:
            with open(output_csv_file, 'w') as f:
                for string in self.extracted_strings:
                    f.write(string + '\n')
            print(f"   CSV File saved to {output_csv_file}")
        else:
            print(f"   CSV File not created, no data found for {self.input_file}")

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
        message = f"******************  An error occurred while transforming {args.input}: ******************"
        length = len(message)
        stars = '*' * length
        marks = '!' * length
        print("   "+stars)
        print("   "+marks)
        print("   "+message)
        exception_type = type(e).__name__
        print(f"   {exception_type}: {e}")
        print("   "+marks)
        print("   "+stars)

if __name__ == "__main__":
    # XMLTransformer.run()
    run()
