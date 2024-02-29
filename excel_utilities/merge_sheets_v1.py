"""
File: merge_sheets.py
Author: Tomasz Krauze
Date: January 18, 2024
Description: This script is designed to consolidate all sheets from multiple Excel files into a single, separate Excel file.
             This script is tailored for customer case scenarios.

"""

import pandas as pd
import os
import sys
import logging
import os
import warnings
import time

start_time = time.time()
warnings.simplefilter("ignore")
logging.basicConfig(level=logging.INFO)

## Start customer-specific variables
# Please customize the following variables based on your specific requirements.

# Unique headers collection with initial hard coded list of headers from Export sheet
export_header = ['ID','PART_ID','EMPTY0','>','Mass','Package Type','Package Material','Package Class','Nb Pins','Package Pitch','Fire Resistance UL','Temperature Min','Temperature Max','Quality Lebel','MSL','Technology','Package Shape','Complexity','Type','Dielectric/Electrolyte','Ceramic Class','Part type/Configuration','Substrat Material']
unique_headers = set(export_header)

# Create collection with first 20 headers order
custom_order = {'PART_ID': 1, 'BCN_NUMBER': 2, 'P_DOC': 3, 'PART_NUMBER': 4, 'ORG_NAME': 5, 'ORG_ID': 6, 'PART_TYPE': 7, 'MANUFACTURING_STATUS': 8, 'LBO_DATE': 9, 'ECC': 10, 'ECCN': 11, 'ECC_DATE': 12, 'A750_INITIAL': 13, 'CLASSIF_INITIAL': 14, 'PPL_STATUS': 15, 'DENOM': 16, 'DESIGN': 17, 'DESCRIPTION_EN': 18, 'ROHS_COMPLIANCE': 19, 'ROHS_EXEMPTION': 20}    
# custom_order = {'ID':1,'PART_ID':2,'NULL':3,'AROW':4,'Mass':5,'Package Type':6,'Package Material':7,'Package Class':8,'Nb Pins':9,'Package Pitch':10,'Fire Resistance UL':11,'Temperature Min':12,'Temperature Max':13,'Quality Lebel':14,'MSL':15,'Technology':16,'Package Shape':17,'Complexity':18,'Type':19,'Dielectric/Electrolyte':20,'Ceramic Class':21,'Part type/Configuration':22,'Substrat Material':23,'one':24,'two':25,'tree':26,'BCN_NUMBER':27,'P_DOC':28,'PART_NUMBER':29,'ORG_NAME':30,'ORG_ID':31,'PART_TYPE':32,'MANUFACTURING_STATUS':33,'LBO_DATE':34,'ECC':35,'ECCN':36,'ECC_DATE':37,'A750_INITIAL':38,'CLASSIF_INITIAL':39,'PPL_STATUS':40,'DENOM':41,'DESIGN':42,'DESCRIPTION_EN':43,'ROHS_COMPLIANCE':44,'ROHS_EXEMPTION':45} 

# End customer-specific variables

# Gettting Excels from path provided in first argument
folder_path = sys.argv[1]
files = os.listdir(folder_path)
excel_files = [file for file in files if file.endswith('.xlsx') or file.endswith('.xls')]

if len(sys.argv) != 2:
    print("Usage: python merge_sheets.py <path>")
    print("For example: python merge_sheets.py C:/Users/xxx/Desktop/excels/src/")
    print("python.exe -m pip install --upgrade pip")
    print("pip install pandas openpyxl xlsxwriter")
    sys.exit(1)

print(f"+------------------------------------------------------------+")
print(f"| Extracting all unique column headers from all Excel sheets |")
print(f"+------------------------------------------------------------+")

# Loop through each Excel file and extract unique column headers
for file in excel_files:
    
    excel_file_path = os.path.join(folder_path, file)
    print(f"Collecting headers from '{excel_file_path}'")

    xls = pd.ExcelFile(excel_file_path)
    sheet_names = xls.sheet_names

    for sn in (sheet_names):

        # Skip EVVs
        if sn in ('EVVs'):
            continue
        
        # Skip empty sheets
        # empty_df = pd.read_excel(excel_file_path, sheet_name=sn, header=None, skiprows=2, nrows=1)
        # if empty_df.empty or empty_df.iloc[0].isna().all():
        #    continue

        try:

            # Read each sheet into a DataFrame
            df = pd.read_excel(excel_file_path, sheet_name=sn, header=0, dtype='str')  # Use the first row as column names

            # Add the column headers to the set
            unique_headers.update(df.columns)

        except (ValueError, TypeError) as e:
            print(f"    Error processing sheet '{sn}' in '{excel_file_path}': {e}")

# Create an empty DataFrame with the unique column headers
merged_df = pd.DataFrame(columns=sorted(list(unique_headers), key=lambda x: custom_order.get(x, float('inf'))))
merged_df.to_excel('merged_data_distinct_headers.xlsx', index=False)
df_join = pd.DataFrame()

print(f"+------------------------------------------------------------+")
print(f"|         Extracting information from all Excel sheets       |")
print(f"+------------------------------------------------------------+")
for file in excel_files:

    excel_file_path = os.path.join(folder_path, file)
    print(f"Extracting data from '{excel_file_path}'")

    # Read Export sheet into a dedicated DataFrame, with hard coded header
    df_export = pd.read_excel(excel_file_path, sheet_name='Export', header=None, skiprows=[0], dtype='str')
    df_export.columns = export_header

    sheet_names = pd.ExcelFile(excel_file_path).sheet_names
    for sn in (sheet_names):

        # Skip EVVs and Export. Export is handled above
        if sn in ('EVVs', 'Export'):
            continue

        try:

            # Read each sheet into a DataFrame
            df = pd.read_excel(excel_file_path, sheet_name=sn, header=0, skiprows=[1], dtype='str')
            merged_df = merged_df._append(df)

        except (ValueError, TypeError) as e:
            print(f"    Error processing sheet '{sn}' in '{excel_file_path}': {e}")

    # Join export sheet with other sheets using PART_ID column
    df_join = df_join._append(pd.merge(df_export, merged_df, on='PART_ID', how='left'))

print(f"+------------------------------------------------------------+")
print(f"|                Saving Data Frames to Excel                 |")
print(f"+------------------------------------------------------------+")

end_time = time.time()
elapsed_time = round(((end_time - start_time) / 60), 2)
print(f"Total extraction time taken: {elapsed_time} minutes")

start_time = time.time()
df_join.to_csv('merged_data_distinct_headers.csv', index=False)
end_time = time.time()
elapsed_time = round((end_time - start_time), 2)
print(f"Export to csv time taken   : {elapsed_time} seconds")

start_time = time.time()
df_join.to_excel('merged_data_distinct_headers.xlsx', index=False)
end_time = time.time()
elapsed_time = round(((end_time - start_time) / 60), 2)
print(f"Export to Excel time taken : {elapsed_time} minutes")