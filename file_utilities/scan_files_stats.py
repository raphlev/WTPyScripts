import os
import csv
from openpyxl import Workbook

# File types to track (including both text and binary files)
file_types = [
    'acl', 'alias', 'amo', 'asv', 'bcf', 'ccf', 'cgm', 'class', 'csv', 'db', 'dcf', 'dcl',
    'disabledfordeployment', 'dll', 'docx', 'dtd', 'ent', 'exe', 'fos', 'genfos', 'gif', 'h',
    'htm', 'ism', 'jar', 'java', 'jpg', 'js', 'jsfrag', 'jsp', 'jspf', 'lst', 'old', 'oncheckin_corrected',
    'pcf', 'png', 'properties', 'rbinfo', 'sch', 'sql', 'style', 'tif', 'tld', 'tpl', 'txt',
    'unused', 'xconf', 'xlf', 'xml', 'xsd', 'xsl', 'xslt', 'zip'
]

# Create dictionary to store file statistics
file_stats = {file_type: {'count': 0, 'lines': 0, 'size': 0} for file_type in file_types}

# List of processed files
processed_files = []

def get_line_count(file_path):
    """Attempts to count the lines in a file. Skips if the file is binary or an error occurs."""
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
            return sum(1 for line in file)
    except Exception:
        # Skip the file if it's binary or unreadable
        return 0

def process_directory(root_dir):
    """Scans the directory for files, updates statistics, and manages file list."""
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_ext = file.lower().split('.')[-1]  # Get the file extension
            file_path = os.path.join(root, file)

            if file_ext in file_stats:
                # Update the number of files for the file type
                file_stats[file_ext]['count'] += 1
                
                # Update the size of files for the file type
                try:
                    file_size = os.path.getsize(file_path)
                    file_stats[file_ext]['size'] += file_size
                except Exception:
                    file_size = 0
                
                # Attempt to count the number of lines for all files
                line_count = get_line_count(file_path)
                file_stats[file_ext]['lines'] += line_count

                # Add file to the processed files list
                processed_files.append(file_path)

def save_to_excel(output_file):
    """Saves the statistics to an Excel file"""
    wb = Workbook()
    ws = wb.active
    ws.title = "File Stats"

    # Write the header row
    header = ['File Type', 'Number of Files', 'Total Lines', 'Total Size (bytes)']
    ws.append(header)

    # Write the statistics for each file type
    for file_type, stats in file_stats.items():
        if stats['count'] > 0:  # Only include file types with non-zero counts
            ws.append([file_type, stats['count'], stats['lines'], stats['size']])

    # Save the Excel file
    try:
        wb.save(output_file)
        print(f"Excel file '{output_file}' saved successfully.")
    except Exception as e:
        print(f"Error saving Excel file: {e}")

def save_processed_files_list(csv_file):
    """Saves the processed files list to a CSV file."""
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['File Path'])
            for file_path in processed_files:
                writer.writerow([file_path])
        print(f"Processed files list saved to '{csv_file}' successfully.")
    except Exception as e:
        print(f"Error saving processed files list: {e}")

def remove_csv_file(csv_file):
    """Removes the CSV file after processing is complete."""
    try:
        if os.path.exists(csv_file):
            os.remove(csv_file)
            print(f"CSV file '{csv_file}' removed successfully.")
    except Exception as e:
        print(f"Error removing CSV file: {e}")

if __name__ == "__main__":
    # Define the root directory to scan and output files
    root_dir = r'C:\Users\levequer\Downloads'  # Replace with your folder path
    excel_output_file = 'file_stats_output.xlsx'
    csv_output_file = 'processed_files_list.csv'

    # Process the directory and gather statistics
    process_directory(root_dir)

    # Save the results to Excel and CSV
    save_to_excel(excel_output_file)
    save_processed_files_list(csv_output_file)

    # Remove the CSV file after processing
    remove_csv_file(csv_output_file)
