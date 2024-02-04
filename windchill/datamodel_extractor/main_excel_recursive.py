"""
File: extract_xml_transformer.py
Author: Raphael Leveque
Date: November , 2023
Description: See README. Intended to be used to transform Windchill configuration file into excel, this script is the entry point for processing directories recursively. It creates Excel files from XML files found in the specified input directory and its subdirectories. It creates an excel file per each subdirectories found with valid input XML files.
"""

import os
import argparse
import logging
from extract_excel_processor import ExcelFileProcessor

class RecursiveExcelFileCreator:
    def __init__(self, root_input_dir, root_output_dir, keep_csv=False):
        self.root_input_dir = root_input_dir
        self.root_output_dir = root_output_dir
        self.keep_csv = keep_csv
        logging.info('   ------------------------------BEGIN RECURSIVE LOOP----------------------------------')

    def __del__(self):
        logging.info('   ------------------------------END   RECURSIVE LOOP---------------------------------')

    def process_directory(self, input_dir, output_dir):
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Process the files in the current directory
        processor = ExcelFileProcessor(input_dir, output_dir, self.keep_csv)
        processor.process_excel_file()

    def process_all_subdirectories(self):
        # Process files directly in the root input directory first
        self.process_directory(self.root_input_dir, self.root_output_dir)

        # Now process files in all subdirectories
        for root, dirs, _ in os.walk(self.root_input_dir):
            for dir in dirs:
                input_subdir = os.path.join(root, dir)
                output_subdir = os.path.join(self.root_output_dir, os.path.relpath(input_subdir, self.root_input_dir))
                self.process_directory(input_subdir, output_subdir)

    @staticmethod
    def run():
        try:
            parser = argparse.ArgumentParser(description="Recursively process XML files and generate Excel workbooks.")
            parser.add_argument('-i', '--input_dir', required=True, help='Root input directories containing XML files (Types, Enum, Classification).')
            parser.add_argument('-o', '--output_dir', required=True, help='Root output directory for Excel files.')
            parser.add_argument('--keep_csv', action='store_true', help='Optional: keep CSV files after processing')

            args = parser.parse_args()

            recursive_creator = RecursiveExcelFileCreator(args.input_dir, args.output_dir, args.keep_csv)
            recursive_creator.process_all_subdirectories()
        except Exception as e:
            message = f"******************  Process recursively excel files failed: ******************"
            length = len(message)
            stars = '*' * length
            marks = '!' * length
            logging.info(stars)
            logging.info(marks)
            logging.info(message)
            exception_type = type(e).__name__
            logging.info(f"{exception_type}: {e}")
            logging.exception("Exception: ")
            logging.info(marks)
            logging.info(stars)

if __name__ == "__main__":
    RecursiveExcelFileCreator.run()
