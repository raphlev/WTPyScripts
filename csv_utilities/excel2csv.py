"""
File: excel2csv.py
Author: Tomasz Krauze
Description: This script is designed to convert from xlsx to csv, rename csv and ensure that all files has UTF-8 encoding
Changelog:
v1 - init

"""

import pandas
import os
import sys
import logging
import os
import warnings
import time
import codecs
import shutil

start_time = time.time()
warnings.simplefilter("ignore")
logging.basicConfig(level=logging.INFO)

# Gettting Excels from path provided in first argument
folder_path = sys.argv[1]

if len(sys.argv) != 2:
    print("Usage: python excel2csv.py <path>")
    print("For example: python.exe excel2csv.py C:/Users/xxx/Desktop/excels/src/")
    print("python.exe -m pip install --upgrade pip")
    print("pip install pandas openpyxl xlsxwriter")
    sys.exit(1)

print(f"+------------------------------------------------------------+")
print(f"|                  Extracting Excels to CSVs                 |")
print(f"+------------------------------------------------------------+")


print(f"1._________________ Classification mapping ___________________")
excel_file_path=os.path.join(folder_path, "3.Transform_WC__MappingClassification-v1.xlsx")
df = pandas.read_excel(excel_file_path, skiprows=6, dtype='str', sheet_name='Mapping-Classif')
# Check if the "|" character exists in the cell value
for column in df.columns:
    for index, value in df[column].items():
        if isinstance(value, str) and "|" in value:
            print("| pipe character exists in Excel !!")
df = df.iloc[:, :9]
csv_file_path=os.path.join(folder_path, "3.Transform_WC__MappingClassification-v1.csv")
df.to_csv(csv_file_path, index=False, sep='|', encoding='ansi')
with codecs.open(csv_file_path, 'r', encoding='ansi') as file:
    content = file.read()
with codecs.open(csv_file_path, 'w', encoding='utf-8') as file:
    file.write(content)


print(f"2.______________________ TCIS symbols ________________________")
# !!!! For this particular Excel convert all cells to TXT in Excel !!!!
excel_file_path=os.path.join(folder_path, "1.Extract_TCIS__Symbols.xlsx")
df = pandas.read_excel(excel_file_path, dtype='str', sheet_name='Export')
# Check if the "|" character exists in the cell value
for column in df.columns:
    for index, value in df[column].items():
        if isinstance(value, str) and "|" in value:
            print("| pipe character exists in Excel !!")
selected_columns = [0, 1, 4, 5, 6, 7]
df = df.iloc[:, selected_columns]
csv_file_path=os.path.join(folder_path, "2.Cleanse_TCIS__Symbols.csv")
df.to_csv(csv_file_path, index=False, sep='|', encoding='utf-8')


print(f"3._____________________ Missing TAES PN ______________________")
excel_file_path=os.path.join(folder_path, "1.Extract_TCIS__MissingTAES_PN.xlsx")
df = pandas.read_excel(excel_file_path, dtype='str', sheet_name='trouvé')
# Check if the "|" character exists in the cell value
for column in df.columns:
    for index, value in df[column].items():
        if isinstance(value, str) and "|" in value:
            print("| pipe character exists in Excel !!")
csv_file_path=os.path.join(folder_path, "2.Cleanse_TCIS__MissingTAES_PN.csv")
df.to_csv(csv_file_path, index=False, sep='|', encoding='utf-8')


print(f"4._________________ Standard Reference Parts _________________")
excel_file_path=os.path.join(folder_path, "1.Extract_SAP__StandardReferenceParts.xlsx")
df = pandas.read_excel(excel_file_path, dtype='str', sheet_name='Feuil1')
# Check if the "|" character exists in the cell value
for column in df.columns:
    for index, value in df[column].items():
        if isinstance(value, str) and "|" in value:
            print("| pipe character exists in Excel !!")
csv_file_path=os.path.join(folder_path, "2.Cleanse_SAP__StandardReferenceParts.csv")
df.to_csv(csv_file_path, index=False, sep='|', encoding='utf-8')


print(f"5._________________ Copy ManufacturerParts ___________________")
new_destination = os.path.join(folder_path, "2.Cleanse_SAP__ManufacturerParts.csv")
shutil.copyfile(os.path.join(folder_path, "1.Extract_SAP__ManufacturerParts.csv"), new_destination)
with codecs.open(new_destination, 'r', encoding='utf-8', errors='ignore') as file:
	content = file.read()
with codecs.open(new_destination, 'w', encoding='utf-8') as new_file:
	new_file.write(content)
      

print(f"6.__________________ Copy StandardDocument ___________________")
new_destination = os.path.join(folder_path, "2.Cleanse_SAP__StandardDocument.csv")
shutil.copyfile(os.path.join(folder_path, "1.Extract_SAP__StandardDocument.csv"), new_destination)
with codecs.open(new_destination, 'r', encoding='utf-8', errors='ignore') as file:
	content = file.read()
with codecs.open(new_destination, 'w', encoding='utf-8') as new_file:
	new_file.write(content)


print(f"7.____________________ Copy StandardParts ____________________")
new_destination = os.path.join(folder_path, "2.Cleanse_SAP__StandardParts.csv")
shutil.copyfile(os.path.join(folder_path, "1.Extract_SAP__StandardParts.csv"), new_destination)
with codecs.open(new_destination, 'r', encoding='utf-8', errors='ignore') as file:
	content = file.read()
with codecs.open(new_destination, 'w', encoding='utf-8') as new_file:
	new_file.write(content)


print(f"8._________________ Copy TCIS PartsDocuments _________________")
new_destination = os.path.join(folder_path, "2.Cleanse_TCIS__Parts_Documents.csv")
shutil.copyfile(os.path.join(folder_path, "1.Extract_TCIS__Parts_Documents.csv"), new_destination)
with codecs.open(new_destination, 'r', encoding='utf-8', errors='ignore') as file:
	content = file.read()
with codecs.open(new_destination, 'w', encoding='utf-8') as new_file:
	new_file.write(content)