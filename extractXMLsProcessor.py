import os
import argparse
import sys
from pathlib import Path
from extractXMLTransformer import XMLTransformer

class XMLFilesProcessor:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        # Ensure output directory exists
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def process_files(self):
        # Iterate through all files in the input directory
        for file in os.listdir(self.input_dir):
            # Check if the file is an XML file
            if file.endswith(".xml"):
                self._process_file(file)

    def _process_file(self, file):
        input_file_path = os.path.join(self.input_dir, file)
        # Construct the output file name by replacing the .xml extension with .csv
        output_file_name = os.path.splitext(file)[0] + '.csv'
        output_file_path = os.path.join(self.output_dir, output_file_name)

        try:
            transformer = XMLTransformer(input_file_path, output_file_path)
            transformer.transform()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run():
        # Set up command line argument parsing
        parser = argparse.ArgumentParser(description="Process all XML files from input folder and output CSV files.")
        parser.add_argument('-i', '--input_dir', type=str, required=True, help="Input folder containing XML files")
        parser.add_argument('-o', '--output_dir', type=str, required=True, help="Output folder for CSV/EXCEL files")

        args = parser.parse_args()

        try:
            # Create XMLFilesProcessor instance and process files
            processor = XMLFilesProcessor(args.input_dir, args.output_dir)
            processor.process_files()
            print("All files have been processed.")
        except Exception as e:
            print(f"An error occurred during processing: {e}")
            sys.exit(1)

if __name__ == "__main__":
    XMLFilesProcessor.run()
