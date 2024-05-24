"""
File: extract_xml_transformer.py
Author: Raphael Leveque
Date: November , 2023
Description: See README. Intended to be used to transform Windchill configuration file into excel, this script is responsible for transforming one XML file into a specific structured text format. Used as stand-alone, it will create the csv file. It is also used by `extract_excel_processor.py` to create one Excel workbook.
"""

from collections import OrderedDict
import logging
from lxml import etree
import argparse
import os

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(filename)s - %(message)s')

class XMLTransformer:
    def __init__(self, input_file, output_folder, debug=False):
        logging.info('   -------------------------------BEGIN TRANSFORM--------------------------------------')
        self.input_file = input_file
        # Construct the output file name by replacing the .xml extension with .csv
        output_file_name = os.path.splitext(os.path.basename(input_file))[0] + '.csv'
        self.output_file = os.path.join(output_folder, output_file_name)
        self.debug = debug
        self.extracted_strings = [] # Initialize a list to hold the extracted strings
        if self.debug:
                    logging.getLogger().setLevel(logging.DEBUG)

    def __del__(self):
        logging.info('   -------------------------------END   TRANSFORM--------------------------------------')

    def normalize_xml(self, xml_content):
        # Define the replacements as a list of tuples to be executed in same order
        replacements = [
        # TYPES, CLASSIFICATION
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
        # LIFECYCLE
            ('</csvLifeCycleTemplateBegin>', ''),
            ('<csvPhaseTemplateEnd handler="wt.lifecycle.LoadLifeCycle.createPhaseTemplateEnd"></csvPhaseTemplateEnd>', ''),
            ('<csvLifeCycleTemplateEnd handler="wt.lifecycle.LoadLifeCycle.createLifeCycleTemplateEnd"></csvLifeCycleTemplateEnd>', '</csvLifeCycleTemplateBegin>'),
            ('<csvLifeCycleTemplateEnd handler="wt.lifecycle.LoadLifeCycle.createLifeCycleTemplateEnd"/>', '</csvLifeCycleTemplateBegin>'),
        # OIR
            ('<![CDATA[', ''),
            (']]>', ''),
        ]

        # Perform the replacements in order
        for old, new in replacements:
            xml_content = xml_content.replace(old, new)

        return xml_content

    def save_debug_output(self, content):
        debug_output_file =  os.path.splitext(self.output_file)[0] + '_normalized.xml'
        with open(debug_output_file, 'w') as f:
            f.write(content)
        logging.debug(f"   Debug output saved to {debug_output_file}")

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
            classifications = types = False

            for element in begin_types:
                if element.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCTYPE']"):
                    types = True
                    break
                elif element.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCSTRUCT']"):
                    classifications = True
                    break
            
            if types:
                logging.info('   Processing Types XML(encoding utf-8): ' + self.input_file)
                self.extract_data_type(root)
            elif classifications:
                logging.info('   Processing Classification XML(encoding utf-8): ' + self.input_file)
                self.extract_data_classification(root)
            elif root.xpath(".//csvBeginEnumMemberView"):
                logging.info('   Processing Global Enumeration XML(encoding utf-8): ' + self.input_file)
                self.extract_data_enum(root)
            elif root.xpath(".//csvLifeCycleTemplateBegin"):
                logging.info('   Processing Lifecycle XML(encoding utf-8): ' + self.input_file)
                self.extract_data_lc(root)
            elif root.xpath(".//TypeBasedRule"):
                logging.info('   Processing OIR XML(encoding utf-8): ' + self.input_file)
                self.extract_data_oir(root)
            else:
                logging.info('   Unknown XML structure detected (encoding utf-8):' + self.input_file)
                # Placeholder for future functionality

            # Write the extracted strings to the output file
            self.write_output(self.output_file)
        except Exception as e:
            message = f"******************  Transform xml file failed: ******************"
            length = len(message)
            stars = '*' * length
            marks = '!' * length
            logging.info("   "+stars)
            logging.info("   "+marks)
            logging.info("   "+message)
            exception_type = type(e).__name__
            logging.info(f"   {exception_type}: {e}")
            logging.exception("   Exception:")
            logging.info("   "+marks)
            logging.info("   "+stars)

    def extract_data_enum(self, root):
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
            header_line = "name~displayName~displayFR"
            self.extracted_strings.append(header_line)
            # Extract information for each 'csvBeginEnumMemberView'
            for enum_member in enum_def_view.xpath(".//csvBeginEnumMemberView"):
                member_info = self.extract_data_enum_member_info(enum_member)
                if member_info:
                    self.extracted_strings.append(member_info)
            # Add an empty row after processing each enum_def_view
            self.extracted_strings.append('<EMPTY_ROW>') 
                   
        return self.extracted_strings

    def extract_data_enum_member_info(self, enum_member):
        member_name = enum_member.xpath("./csvname/text()")[0]
        display_name = enum_member.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")
        display_name = display_name[0] if display_name else '' 
        display_fr = enum_member.xpath("./csvPropertyValue[csvname='displayName']/csvlocale_fr/text()")
        display_fr = display_fr[0] if display_fr else '' 
        selectable = enum_member.xpath("./csvPropertyValue[csvname='selectable'][1]/csvvalue/text()")
        if not display_name or not selectable or selectable[0].lower() == 'false':
            return None
        
        return f"{member_name}~{display_name}~{display_fr}"

    def extract_data_type(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()
        # Prepare the header line for the CSV content
        header_line = "name~display~displayFR~iba~required~type~unit~length~single~upperCase~regularExpr~defaultValue~legalValues~EnumeratedValues"

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
                    self.extracted_strings.extend(self.extract_attribute_definitions(attr_def_view, '', '', 0, instantiable, '', '', '', '', '', mode='Types'))

            # Add an empty row after processing each type_def_view
            self.extracted_strings.append('<EMPTY_ROW>') 

        # Remove all content if no attributes found to prevent any csv file with empty value
        if len(self.extracted_strings) == 4 and self.extracted_strings[3]== '<EMPTY_ROW>' :
            self.extracted_strings.clear()

        return self.extracted_strings

    def extract_data_classification(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()

        # Prepare the header line for the CSV content
        header_line = "Family~depth~classifType~parentClassifType~instantiable~displayClassifType~displayClassifTypeFR~descriptionType~descriptionTypeFR~attributeName~attributeDisplayName~attributeDisplayNameFR~iba~required~type~unit~length~single~upperCase~regularExpr~defaultValue~legalValues~EnumeratedValues"
        self.extracted_strings.append(header_line)

        # keep track of typeObject and its depth
        type_depth_map = {}
        type_attributes_map = {}  # Map to store the attributes of each type

        # Calculate Family
        Family = "ROOT"
        
        # Iterate over each csvBeginTypeDefView element
        for type_def_view in root.xpath(".//csvBeginTypeDefView[csvattTemplate='LWCSTRUCT']"):
            typeObject = parentType = displayType = displayTypeFR = descriptionType = descriptionTypeFR = ''
            instantiable = 'No'
            name = display = displayFR = iba = datatype = length = unit = defaultValue = list_value = enum_members = regularExpr = ''
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

            displayTypeFR = type_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvlocale_fr/text()")
            displayTypeFR = displayTypeFR[0] if displayTypeFR else ''


            descriptionType = type_def_view.xpath("./csvPropertyValue[csvname='description']/csvvalue/text()")
            descriptionType = descriptionType[0] if descriptionType else ''

            descriptionTypeFR = type_def_view.xpath("./csvPropertyValue[csvname='description']/csvlocale_fr/text()")
            descriptionTypeFR = descriptionTypeFR[0] if descriptionTypeFR else ''
 
            # Calculate depth
            depth = 0
            current_parent = parentType
            while current_parent:
                depth += 1
                current_parent = type_depth_map.get(current_parent, None)

            if str(depth) == "2":
                Family = typeObject

            type_depth_map[typeObject] = parentType  # Map current type to its parent

            # Prepare the type line
            type_line = f"{Family}~{depth}~{typeObject}~{parentType}~{instantiable}~{displayType}~{displayTypeFR}~{descriptionType}~{descriptionTypeFR}~{name}~{display}~{displayFR}~{iba}~{required}~{datatype}~{unit}~{length}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}"

            # Extract current attributes
            current_attributes = []
            for attr_def_view in type_def_view.xpath("./csvBeginAttributeDefView"):
                current_attributes.extend(self.extract_attribute_definitions(attr_def_view, typeObject, parentType, depth, Family, instantiable, displayType, displayTypeFR, descriptionType, descriptionTypeFR, 'Classification'))

            # Update and append ancestor attributes with current node's depth and other values
            ancestor_attributes = []
            if parentType in type_attributes_map:
                for attr in type_attributes_map[parentType]:
                    updated_attr = attr.split("~")
                    # Update depth and keep current node's type, parentType, instantiable, and displayType, and displayTypeFR, and Family
                    updated_attr[0] = Family
                    updated_attr[1] = str(depth)
                    updated_attr[2] = typeObject
                    updated_attr[3] = parentType
                    updated_attr[4] = instantiable
                    updated_attr[5] = displayType
                    updated_attr[6] = displayTypeFR
                    updated_attr[7] = descriptionType
                    updated_attr[8] = descriptionTypeFR
                    ancestor_attributes.append("~".join(updated_attr))

            # Combine the ancestor and current attributes
            combined_attributes = ancestor_attributes + current_attributes
            # Sort the list based on the attributeName: 10th position (index 9)
            combined_attributes.sort(key=lambda x: x.split("~")[9])

            # Remove duplicates for entire row while maintaining order - this my not be necessary at this point
            unique_attributes = list(OrderedDict.fromkeys(combined_attributes))

            # Apply merging to get unique properties definition
            # Preserve explicit definitions when inherited properties are overridden from ancestors
            merged_and_unique_attributes = self.merge_attributes_with_override(header_line,unique_attributes)
            # Sort the list based on the attributeName: 10th position (index 9)
            merged_and_unique_attributes.sort(key=lambda x: x.split("~")[9])

            # Append the sorted and unique attributes, starting with the type line
            self.extracted_strings.append(type_line)
            #self.extracted_strings.extend(unique_attributes)
            self.extracted_strings.extend(merged_and_unique_attributes)

            # Store the current and ancestor attributes for future use
            #type_attributes_map[typeObject] = unique_attributes
            type_attributes_map[typeObject] = merged_and_unique_attributes

        # else:
        #     logging.info('Type non instantiable for : '+self.output_file+' - File not created !')

        # remove if only header to prevent csv file with empty value
        if len(self.extracted_strings) == 1:
            self.extracted_strings.clear()
        return self.extracted_strings

    def merge_attributes_with_override(self,header_line,unique_attributes):
        # Define which columns are boolean; indexes based on zero-based indexing after 'attributeName'
        boolean_columns = [index for index, column_name in enumerate(header_line.split("~")) if column_name in {"required", "single", "upperCase"}]
        
        # Group attributes by their identifying key (first 10 columns)
        attribute_groups = {}
        for attribute in unique_attributes:
            attr_parts = attribute.split("~")
            key = tuple(attr_parts[:10])  # Key based on first 10 fields Family,depth,classifType,parentClassifType,instantiable,displayClassifType,displayClassifTypeFR,description,descriptionTypeFR,attributeName
            if key not in attribute_groups:
                attribute_groups[key] = []
            attribute_groups[key].append(attr_parts)
        
        merged_attributes = []
        for key, group in attribute_groups.items():
            merged_row = group[0]  # Start with the first row in the group
            for attr_parts in group[1:]:
                for i, value in enumerate(attr_parts):
                    if i >= 10:  # Only merge attributes after the 10th column
                        if i in boolean_columns:
                            # Apply Merge Rule for boolean values: if any "Yes" value exists among duplicates, the merged result will also be "Yes"
                            if value == "Yes" or merged_row[i] == "Yes":
                                merged_row[i] = "Yes"
                        else:
                            # Apply Merge Rule for non-boolean values: the first non-empty value encountered is kept
                            if value:  # If the current value is non-empty, check if it should override
                                merged_row[i] = value if merged_row[i] == "" else merged_row[i]
            merged_attributes.append("~".join(merged_row))
        
        return merged_attributes

    def extract_attribute_definitions(self, attr_def_view, typeObject, parentType, depth, Family, instantiable, displayType, displayTypeFR, descriptionType, descriptionTypeFR, mode):
            name = display = displayFR = class_value = datatype = length = unit = defaultValue = list_value = enum_members = regularExpr = ''
            required = single = upperCase = iba = 'No'
            attributes = []
            # Process for name, class, defaultValue, dataType and unit
            if attr_def_view.findtext('./csvIBA'):
                iba = 'Yes'
            name = attr_def_view.findtext('./csvname') or ''

            # Process for required, single, upperCase, length, unit

            display = attr_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvvalue/text()")
            display = display[0] if display else ''

            displayFR = attr_def_view.xpath("./csvPropertyValue[csvname='displayName']/csvlocale_fr/text()")
            displayFR = displayFR[0] if displayFR else ''

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
                                    enum_members = enum_members + ': ' + self.extract_data_type_member_names(constraint_def_view) # List of values with selectable=yes

            # Replace length with default value for String if empty (information not available in XML)
            if length == '' and datatype == 'String':
                length = '500'
            elif length.startswith('0-'):
                length = length.replace('0-', '', 1) # Update format of value 

            # Append the extracted attributes as a new line
            if mode == 'Classification':
                attributes.append(f"{Family}~{depth}~{typeObject}~{parentType}~{instantiable}~{displayType}~{displayTypeFR}~{descriptionType}~{descriptionTypeFR}~{name}~{display}~{displayFR}~{iba}~{required}~{datatype}~{unit}~{length}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}")
            elif mode == 'Types':
                attributes.append(f"{name}~{display}~{displayFR}~{iba}~{required}~{datatype}~{unit}~{length}~{single}~{upperCase}~{regularExpr}~{defaultValue}~{list_value}~{enum_members}")

            return attributes

    def extract_data_type_member_names(self, constraint_def_view):
        member_names = []
        # Start from the constraint definition view and iterate through following elements
        for enum_def_view in constraint_def_view.xpath("./csvBeginEnumDefView[1]"):
            for enum_member in enum_def_view.xpath(".//csvBeginEnumMemberView"):
                member_name = enum_member.xpath("./csvname/text()")[0]
                selectable = enum_member.xpath("./csvPropertyValue[csvname='selectable'][1]/csvvalue/text()")
                if member_name and selectable[0].lower() == 'true':
                    member_names.append(member_name)
        return '|'.join(member_names)

    def extract_data_lc(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()
        for lc_template in root.xpath(".//csvLifeCycleTemplateBegin"):
            # Extract the displayName value
            display = lc_template.xpath("./csvname/text()")[0] or ''
            self.extracted_strings.append(display)
            # Prepare the header line for the CSV content
            header_line = "name~displayName"
            self.extracted_strings.append(header_line)
            # Extract information for each 'csvPhaseTemplateBegin'
            for phase in lc_template.xpath(".//csvPhaseTemplateBegin"):
                phase_name = phase.xpath("./csvname/text()")
                phase_name = phase_name[0] if phase_name else ''
                phase_state = phase.xpath("./csvphaseState/text()")
                phase_state = phase_state[0] if phase_state else ''
                self.extracted_strings.append(f"{phase_state}~{phase_name}")
            # Add an empty row after processing each lc_template
            self.extracted_strings.append('<EMPTY_ROW>') 
                   
        return self.extracted_strings

    def extract_data_oir(self, root):
        # Clear the list for new data
        self.extracted_strings.clear()
        for base_rule in root.xpath(".//TypeBasedRule"):
            # Extract the displayName value
            rule_name = base_rule.xpath(".//ruleName/text()")[0] or ''
            self.extracted_strings.append(rule_name)
            # Prepare the header line for the CSV content
            header_line = "objType~folder.id~lc.id~versioning~numbering"
            self.extracted_strings.append(header_line)
            # Extract information for each 'AttributeValues'
            for attr_values in base_rule.xpath(".//AttributeValues"):
                obj_type = attr_values.xpath("./@objType")[0] or ''
                folder_id = attr_values.xpath('.//AttrValue[@id="folder.id"]/Arg/text()')
                folder_id = folder_id[0] if folder_id else ''
                lc_id = attr_values.xpath('.//AttrValue[@id="lifeCycle.id"]/Arg/text()')
                lc_id = lc_id[0] if lc_id else ''
                versioning = attr_values.xpath('.//AttrValue[@id="MBA|versionInfo"]/Arg/text()')
                versioning = versioning[0] if versioning else ''
                args_numbering = attr_values.xpath('.//AttrValue[@id="number"]/Arg/text()')
                numbering = ''.join(args_numbering) if args_numbering else ''
                self.extracted_strings.append(f"{obj_type}~{folder_id}~{lc_id}~{versioning}~{numbering}")
            # Add an empty row after processing each base_rule
            self.extracted_strings.append('<EMPTY_ROW>') 
                   
        return self.extracted_strings

    def write_output(self,output_csv_file):
        if self.extracted_strings:
            with open(output_csv_file, 'w', encoding='utf-8') as f:
            # with open(output_csv_file, 'w') as f:
                for string in self.extracted_strings:
                    f.write(string + '\n')
            logging.info(f"   CSV File created (encoding utf-8): {output_csv_file}")
        else:
            logging.info(f"   CSV File not created, no data found for {self.input_file}")

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
        logging.info("   "+stars)
        logging.info("   "+marks)
        logging.info("   "+message)
        exception_type = type(e).__name__
        logging.info(f"   {exception_type}: {e}")
        logging.exception("   Exception:")
        logging.info("   "+marks)
        logging.info("   "+stars)

if __name__ == "__main__":
    # XMLTransformer.run()
    run()
