# Windchill Data Model Information Extraction Scripts
Author: Raphael Leveque

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
This will create new .\output\ directory with additional subfoders containing different excel files related to the input folder structure. Because optional --keep_csv argument is not used, all generated csv files have been removed from each output folders.

### extract_excel_processor.py
To process XML files and generate Excel workbooks:
```bash
python extract_excel_processor.py -i [INPUT_DIR] -o [OUTPUT_DIR] [--keep_csv]
```
- `-i` or `--input_dir`: Input directory containing XML files.
- `-o` or `--output_dir`: Output directory for CSV and Excel files.
- `--keep_csv`: (Optional) Keep CSV files after processing.

Example:
```bash
python .\windchill_datamodel_extractor\extract_excel_processor.py -i .\input\Types -o .\output\Types
```
This will create new .\output\Types\ directory with one resulted excel file. Because optional --keep_csv argument is not used, all generated csv files have been removed from output folder.

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
python .\windchill_datamodel_extractor\extract_xml_transformer.py -i .\input\Classification\Classification.xml -o .\output\Test\ --debug
```
This will create new .\output\Test\ directory with one resulted csv file. Because optional --debug argument is used, Classification_normalized.xml file is also created to verify the normalized xml content generated from input xml file being processed.

## Script Descriptions
### 1. main_excel_recursive.py
This script is the entry point for processing directories recursively. It creates Excel files from XML files found in the specified input directory and its subdirectories. It creates an excel file per each subdirectories found with valid input XML files.

### 2. extract_excel_processor.py
This script takes in a directory of several XML files, processes them, and generates one Excel workbook with a Table of Content. Used as stand-alone, it will create one excel file. It is also used by `main_excel_recursive.py` to create several Excel workbooks.

### 3. extract_xml_transformer.py
This script is responsible for transforming one XML file into a specific structured text format. Used as stand-alone, it will create the csv file. It is also used by `extract_excel_processor.py` to create one Excel workbook. It currently supports Enumerations, Types, Classification, Lifecycle and OIR XML files.



#### Overview of XML Transformation Script

This script is designed to process XML export files from  Windchill, with functionality for managing classifications, types, Object Initialization Rules (OIR), and Lifecycle configurations. It is a tool for extracting, transforming, and flattening hierarchical XML data into a structured CSV format, which can be imported in excel file.

##### Key Components

- **Classification Management**: Handles the extraction of hierarchical classifications, transforming them into a flat structure. This process includes managing depth calculations and inheritance of attributes from parent to child nodes.

- **Type Handling**: Processes type definitions within the XML, extracting essential properties and characteristics. This functionality supports the detailed analysis and mapping of type-specific data.

- **OIR Processing**: Extracts and processes Object Initialization Rules from the XML.

- **Lifecycle Configuration**: Manages the extraction of lifecycle configurations (states only).

##### Shared Functionality

- **`extract_attribute_definitions` Function**: used across both classification and type management. This function extracts detailed property definitions, such as attribute names, display names, data types, and constraints, ensuring a comprehensive capture of the XML's semantic structure.

##### Usage and Integration

This script transforms Windchill XML exports into structured CSV files.

#### 3.1 highlight classification xml parsing logic: extract_data_classification Function Overview

The `extract_data_classification` function is designed to extract relevant information from Windchill Classification XML export file and transforming it into a flattened CSV format.

##### Key Processes

1. **Track Object Depth**: Initializes `type_depth_map` to keep track of each object's depth within the XML hierarchy, facilitating the understanding of parent-child relationships.

2. **Iterate Over Elements**: Processes each `csvBeginTypeDefView` element found in the XML, extracting and handling data for individual objects, including their type, parent type, and display attributes.

3. **Update and Append Ancestor Attributes**: For each object, ancestor attributes are updated with the current object's depth and other specific values, ensuring that inherited properties are accurately reflected.

4. **Combine Ancestor and Current Attributes**: Merges attributes from ancestor objects with those of the current object, preparing for a unified representation in the CSV output.

5. **Remove Duplicates While Maintaining Order**: Utilizes an `OrderedDict` to remove duplicate entries based on the entire row, preserving the order of attributes which is crucial for subsequent processing steps.

6. **Apply Merging for Unique Property Definitions**: Implements a merging strategy to handle overridden properties from ancestors, ensuring that the most relevant definitions are preserved in cases of attribute inheritance.

7. **Sort Attributes by Name**: Orders the combined attributes list based on the `attributeName`, facilitating readability and consistency in the CSV output.

8. **Append Sorted and Unique Attributes**: Adds the processed attributes to the CSV content, starting with a predefined type line that includes essential object information.

9. **Store Current and Ancestor Attributes for Future Use**: Updates `type_attributes_map` with the processed attributes for each object, allowing for  access and reuse in processing subsequent objects.

##### Logic and Features

- The function employs XPath queries to selectively process elements within the XML, focusing on those relevant for classification purposes.
- Depth calculation for understanding the hierarchical structure, with special handling to designate objects at depth 2 as "Family" heads.
- Ancestor attributes are updated and merged, with specific rules applied to handle boolean and non-boolean properties, ensuring accurate representation of inherited and overridden attributes.
- The function ensures that the final CSV output is not only accurately representative of the hierarchical data but also organized and readable, with considerations for attribute order and uniqueness.

##### type depth calculation logic

- The purpose of the type_depth_map in extract_data_classification function is to keep track of the depth of each object (or type) in the hierarchical structure of your XML data. Here's a breakdown of how the depth calculation works and what type_depth_map stores:
- Track Parent-Child Relationships: It maps each object (identified by typeObject) to its parent (parentType). This mapping is essential for understanding the hierarchy of objects in your XML structure.
- Calculate Depth: The depth of an object indicates its level in the hierarchy, with the root object starting at depth 0. Child objects have a depth of 1, grandchildren have a depth of 2, and so on. This hierarchical depth is crucial for organizing data, especially when transforming hierarchical structures into flat structures like CSVs.
- How Depth is Calculated: Initialization: The depth variable for each object starts at 0. Traversing Upwards: For each object, the function looks up its parent in type_depth_map. If a parent is found, depth is incremented by 1, and the function continues to look up the parent of this parent, incrementing depth each time. This process repeats until a parent is not found in the map, which means the current object is at the top level of its hierarchy.
- Setting the Family Attribute: If the depth is 2, it sets the Family variable to the current typeObject. This implies that objects at depth 2 are considered to be "family" heads in your specific context.
- Storing in the Map: After calculating the depth, the function updates type_depth_map by mapping the current typeObject to its parentType. This step is crucial for the depth calculation of subsequent objects.
- Example
-- Root (depth 0)
--- Child1 (depth 1)
---- Grandchild1 (depth 2)
- When processing Grandchild1, the function looks up Child1 in type_depth_map, finds it, increments depth to 1, then looks up Root, finds it, increments depth to 2, and then stops as Root has no parent. Grandchild1's depth is now correctly calculated as 2.
- The type_depth_map is a dictionary where keys are object types (typeObject) and values are their parent types (parentType). It is used to calculate the depth of each object by tracking how many levels up the hierarchy it is from the root. This depth calculation allows you to understand the hierarchical structure of your data, which is particularly useful when flattening the structure for a CSV output. The depth information, combined with the newly introduced Family attribute, enables you to maintain a connection to the hierarchical context of each object, even in the flattened CSV format.
