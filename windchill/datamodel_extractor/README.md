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
This script is responsible for transforming one XML file into a specific structured text format. Used as stand-alone, it will create the csv file. It is also used by `extract_excel_processor.py` to create one Excel workbook.

#### 3.1 extract_data_classification function - type depth calculation logic

The purpose of the type_depth_map in extract_data_classification function is to keep track of the depth of each object (or type) in the hierarchical structure of your XML data. Here's a breakdown of how the depth calculation works and what type_depth_map stores:

Purpose of type_depth_map:
Track Parent-Child Relationships: It maps each object (identified by typeObject) to its parent (parentType). This mapping is essential for understanding the hierarchy of objects in your XML structure.
Calculate Depth: The depth of an object indicates its level in the hierarchy, with the root object starting at depth 0. Child objects have a depth of 1, grandchildren have a depth of 2, and so on. This hierarchical depth is crucial for organizing data, especially when transforming hierarchical structures into flat structures like CSVs.
How Depth is Calculated
Initialization: The depth variable for each object starts at 0.

Traversing Upwards: For each object, the function looks up its parent in type_depth_map. If a parent is found, depth is incremented by 1, and the function continues to look up the parent of this parent, incrementing depth each time. This process repeats until a parent is not found in the map, which means the current object is at the top level of its hierarchy.

Setting the Family Attribute: If the depth is 2, it sets the Family variable to the current typeObject. This implies that objects at depth 2 are considered to be "family" heads in your specific context.

Storing in the Map: After calculating the depth, the function updates type_depth_map by mapping the current typeObject to its parentType. This step is crucial for the depth calculation of subsequent objects.

Example
Suppose you have a hierarchy like this:

Root (depth 0)
Child1 (depth 1)
Grandchild1 (depth 2)
When processing Grandchild1, the function looks up Child1 in type_depth_map, finds it, increments depth to 1, then looks up Root, finds it, increments depth to 2, and then stops as Root has no parent. Grandchild1's depth is now correctly calculated as 2.

Summary
The type_depth_map is a dictionary where keys are object types (typeObject) and values are their parent types (parentType). It is used to calculate the depth of each object by tracking how many levels up the hierarchy it is from the root. This depth calculation allows you to understand the hierarchical structure of your data, which is particularly useful when flattening the structure for a CSV output. The depth information, combined with the newly introduced Family attribute, enables you to maintain a connection to the hierarchical context of each object, even in the flattened CSV format.

#### 3.2 extract_data_classification function - Update and append ancestor attributes with current node logic

The purpose of the "Update and append ancestor attributes with current node's depth and other values" section of extract_data_classification function is designed to ensure that each node (or object) in your hierarchical data structure inherits attributes from its ancestors. This is a crucial step for flattening a hierarchical structure into a tabular format like CSV, where you want to preserve and display the lineage or inheritance of attributes from parent objects down to their children. Here's a breakdown of what happens in this section:

Purpose
This section aims to:

Inherit Attributes: Ensure that child nodes inherit relevant attributes from their parent nodes. This inheritance includes not just direct parents but all ancestors up the hierarchy.
Maintain Context: By inheriting attributes from ancestors, each node maintains context about where it fits in the overall structure, which is especially important in hierarchical data models.
Update Attributes for the Current Context: Adjust the inherited attributes to reflect the current node's specific details, such as its depth in the hierarchy, its type, and potentially other characteristics that differ from the ancestor.
Process
Here's how the process works in your function:

Check for Ancestor Attributes: The function checks if the current node's parent type (parentType) exists in type_attributes_map. This map is intended to store the attributes of each type, including those inherited from ancestors.

Inherit and Update Attributes: If the parent's attributes are found, it iterates over these attributes. For each attribute, it:

Splits the attribute string (which appears to be concatenated with '~') to access and modify specific attribute values.
Updates certain attributes to reflect the current node's context. This includes setting the Family, updating the depth to the current node's depth, and updating other fields like typeObject, parentType, instantiable, displayType, and displayTypeFR to match the current node.
Re-joins the updated attributes into a single string and appends them to a list of ancestor_attributes, which will then include all updated attributes inherited from the parent, now adjusted for the current node.
Combine and Sort Attributes: After inheriting and updating attributes from ancestors and adding attributes defined directly on the current node (current_attributes), these are combined into a single list. This list is then sorted, typically based on one of the attribute fields, to maintain a consistent order for output. This sorting might be based on the attribute name or another field that helps organize the data meaningfully.

Remove Duplicates: It then removes duplicates from the combined list to ensure that each attribute is only listed once for the current node. This step is crucial because inheritance might introduce duplicate entries for attributes that are common across multiple levels of the hierarchy.

Prepare for Output: Finally, the unique, sorted list of attributes is ready to be appended to the CSV output, starting with the current node's type line. This ensures that the output CSV contains a flat representation of each node, including inherited attributes, properly updated and organized.

Summary
This section is about preserving the hierarchical context in a flat structure by inheriting attributes from ancestors, updating them to reflect the current node's specifics, and preparing them for output. This approach ensures that the flattened CSV representation retains meaningful information about the original hierarchical relationships, enriched by the inherited attributes.
