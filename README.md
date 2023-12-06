
# Windchill Data Model Information Extraction Scripts

## Introduction
This project provides a series of Python scripts to extract Windchill data model information and format the results into Excel files. It currently supports Enumerations, Types, Classification, Lifecycle and OIR XML files.

## Installation
To run these scripts, you will need Python installed on your system along with some external libraries. You can install the required libraries using pip:

```bash
pip install openpyxl lxml argparse
```

## Usage
Each script can be executed independently. Below are the ways to use them:

### main_excel_recursive.py
To run the main script that processes directories recursively:
```bash
python main_excel_recursive.py -i [ROOT_INPUT_DIR] -o [ROOT_OUTPUT_DIR] [--keep_csv]
```
- `-i` or `--input_dir`: Root input directory containing XML files.
- `-o` or `--output_dir`: Root output directory for Excel files.
- `--keep_csv`: (Optional) Keep CSV files after processing.

Example:
```bash
python .\windchill_datamodel_extractor\main_excel_recursive.py -i .\input\ -o .\output\
```
This will create new .output directory with subfoders containing different excel files followin gthe input folder structure.

### extract_excel_processor.py
To process XML files and generate Excel workbooks:
```bash
python extract_excel_processor.py -i [INPUT_DIR] -o [OUTPUT_DIR] [--keep_csv]
```
- `-i` or `--input_dir`: Input directory containing XML files.
- `-o` or `--output_dir`: Output directory for CSV and Excel files.
- `--keep_csv`: (Optional) Keep CSV files after processing.

### extract_xml_transformer.py
To transform an XML file to a text file based on specific rules:
```bash
python extract_xml_transformer.py -i [INPUT_FILE] -o [OUTPUT_FOLDER] [--debug]
```
- `-i` or `--input`: Input XML file path.
- `-o` or `--output`: Output folder.
- `--debug`: (Optional) Enable debug mode to output the normalized XML file.

Example:
```bash
python .\windchill_datamodel_extractor\extract_xml_transformer.py -i .\input\PartTypes\Classification_3.xml -o .\output\Test\ --debug
```
This will create new .\Test\ directory with resulted csv file. Also an xml file is created with content of denormalized xml from input xml file being processed.

## Script Descriptions
### 1. main_excel_recursive.py
This script is the entry point for processing directories recursively. It creates Excel files from XML files found in the specified input directory and its subdirectories.

### 2. extract_excel_processor.py
This script takes in a directory of XML files, processes them, and generates corresponding Excel workbooks with a Table of Contents. Used as stand-alone, it will create one excel file. It is also used by `main_excel_recursive.py` to create several Excel workbooks.

### 3. extract_xml_transformer.py
This script is responsible for transforming XML files into a specific structured text format. Used as stand-alone, it will create the csv files. It is also used by `extract_excel_processor.py` to create one Excel workbook.
