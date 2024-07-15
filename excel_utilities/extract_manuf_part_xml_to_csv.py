"""
This script transforms an XML file with blocks as below:
<csvBeginManufacturerPart handler="com.ptc.windchill.suma.part.LoadPart.beginCreateManufacturerPart" >
    <csvpartName>RESISTANCE 117R +-0,5% 0W125 RS58P</csvpartName>
    <csvpartNumber>CMC-02-82117-005-17</csvpartNumber>
    <csvlifecyclestate>RELEASED</csvlifecyclestate>
    <csvmanufacturerName>CENELEC Electronic Components Committee</csvmanufacturerName>
</csvBeginManufacturerPart>
<csvIBAValue handler="wt.iba.value.service.LoadValue.createIBAValue" >
    <csvdefinition>POWERNote</csvdefinition>
    <csvvalue1>RS58P-RESISTANCE 117R +-0,5% 0W125 RS58P</csvvalue1>
    <csvvalue2></csvvalue2>
    <csvdependency_id></csvdependency_id>
</csvIBAValue>
<csvEndManufacturerPart handler="com.ptc.windchill.suma.part.LoadPart.endCreateManufacturerPart" >
    <csvparentContainerPath>/wt.inf.container.OrgContainer=sep/wt.inf.library.WTLibrary=POWER Manufacturer Parts Library</csvparentContainerPath>
</csvEndManufacturerPart>

into a CSV file with columns:
csvpartName|csvpartNumber|csvlifecyclestate|csvmanufacturerName|POWERNote
"""

import xml.etree.ElementTree as ET
import pandas as pd
import csv

# Function to parse XML and extract required fields
def parse_xml_to_csv(xml_file, csv_file):
    # Parse the XML file with UTF-8 encoding
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize lists to store the extracted data
    part_name = []
    part_number = []
    lifecycle_state = []
    manufacturer_name = []
    power_note = []

    # Temporary variables to store current part information
    current_part_name = None
    current_part_number = None
    current_lifecycle_state = None
    current_manufacturer_name = None

    # Extract the relevant data
    for elem in root:
        if elem.tag == 'csvBeginManufacturerPart':
            current_part_name = elem.find('csvpartName').text
            current_part_number = elem.find('csvpartNumber').text
            current_lifecycle_state = elem.find('csvlifecyclestate').text
            current_manufacturer_name = elem.find('csvmanufacturerName').text
        elif elem.tag == 'csvIBAValue':
            if current_part_name is not None:
                part_name.append(current_part_name)
                part_number.append(current_part_number)
                lifecycle_state.append(current_lifecycle_state)
                manufacturer_name.append(current_manufacturer_name)
                power_note.append(elem.find('csvvalue1').text)
                
                # Reset current part information
                current_part_name = None
                current_part_number = None
                current_lifecycle_state = None
                current_manufacturer_name = None

    # Create a DataFrame from the extracted data
    data = {
        'csvpartName': part_name,
        'csvpartNumber': part_number,
        'csvlifecyclestate': lifecycle_state,
        'csvmanufacturerName': manufacturer_name,
        'POWERNote': power_note
    }
    df = pd.DataFrame(data)

    # Save DataFrame to CSV with UTF-8 encoding, pipe as separator, and without quotes
    df.to_csv(csv_file, index=False, sep='|', quoting=csv.QUOTE_NONE, encoding='utf-8')
    print(f"Data successfully extracted to {csv_file}")

# Example usage
xml_file = r'C:\Users\LT68678\Downloads\createManufacturerParts_CMC_v2.xml' # Use raw string or double backslashes for the file path
csv_file = r'C:\Users\LT68678\Downloads\output.csv' # Use raw string or double backslashes for the file path
parse_xml_to_csv(xml_file, csv_file)
