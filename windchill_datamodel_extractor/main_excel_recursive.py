import os
import argparse
from extract_excel_processor import ExcelFileProcessor

class RecursiveExcelFileCreator:
    def __init__(self, root_input_dir, root_output_dir, delete_csv=False):
        self.root_input_dir = root_input_dir
        self.root_output_dir = root_output_dir
        self.delete_csv = delete_csv

    def process_directory(self, input_dir, output_dir):
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Process the files in the current directory
        processor = ExcelFileProcessor(input_dir, output_dir, self.delete_csv)
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
            parser.add_argument('--delete_csv', action='store_true', help='Optional: delete CSV files after processing')

            args = parser.parse_args()

            recursive_creator = RecursiveExcelFileCreator(args.input_dir, args.output_dir, args.delete_csv)
            recursive_creator.process_all_subdirectories()
        except Exception as e:
            message = f"******************  Process recursively excel files failed: ******************"
            length = len(message)
            stars = '*' * length
            marks = '!' * length
            print(stars)
            print(marks)
            print(message)
            exception_type = type(e).__name__
            print(f"{exception_type}: {e}")
            print(marks)
            print(stars)

if __name__ == "__main__":
    RecursiveExcelFileCreator.run()
