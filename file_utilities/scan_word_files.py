import os
import re
import time
import gc
import functools
import pywintypes
import win32com.client
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def remove_illegal_characters(value):
    if isinstance(value, str):
        # Remove illegal characters (control characters except for allowed ones)
        value = re.sub(
            r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]",
            "",
            value
        )
    return value

# Retry decorator for COM calls with enhanced logging
def retry_on_COM_error(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except pywintypes.com_error as e:
                    if e.args[0] == -2147418111:  # Call was rejected by callee
                        retries += 1
                        print(f"COM call to '{func.__name__}' failed with 'Call was rejected by callee', retrying ({retries}/{max_retries})...")
                        time.sleep(delay)
                    else:
                        print(f"COM error in '{func.__name__}': {e}")
                        raise
                except Exception as e:
                    print(f"Unexpected error in '{func.__name__}': {e}")
                    raise
            print(f"Failed to execute '{func.__name__}' after {max_retries} retries due to COM error.")
            raise Exception(f"Failed to execute '{func.__name__}' after {max_retries} retries due to COM error.")
        return wrapper
    return decorator

# Initialize the Word application
def initialize_word():
    try:
        word_app = win32com.client.Dispatch('Word.Application')
        word_app.Visible = False  # Set to True to make Word visible for debugging
        word_app.DisplayAlerts = False
        word_app.AutomationSecurity = 3  # msoAutomationSecurityForceDisable
        return word_app
    except Exception as e:
        print(f"Error initializing Word application: {e}")
        exit(1)

word = initialize_word()

# Constants for Word
wdStatisticPages = 2

# Create a new Excel workbook and select the active sheet
wb = Workbook()
ws = wb.active
ws.title = "Document Data"

# Write the header row
header = ['Document', 'Directory', 'N# Pages', 'N# Paragraphs', 'Size', 'Objective', 'Scope', 'Content']
ws.append(header)

# Adjust column widths (optional)
column_widths = [30, 100, 20, 20, 20, 50, 50, 50]
for i, column_width in enumerate(column_widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = column_width

# Root directory to scan
root_dir = r'C:\Users\levequer\OneDrive - TRANSITION TECHNOLOGIES PSC S.A\Documents\Backup\Projects\Safran\SAE Indigo\Technical Space\DOCUMENTATION_APPLICATIONS'  # Replace with your folder path

# List to keep track of skipped files
skipped_files = []

# Counter for processed files
file_count = 0

@retry_on_COM_error(max_retries=5, delay=2)
def get_page_count(doc):
    return doc.ComputeStatistics(wdStatisticPages)

@retry_on_COM_error(max_retries=5, delay=2)
def get_paragraph_count(doc):
    return doc.Paragraphs.Count

def get_toc_end_position(doc):
    """
    Returns the end position of the table of contents if it exists, otherwise returns 0.
    """
    try:
        if doc.TablesOfContents.Count > 0:
            toc = doc.TablesOfContents(1)
            toc_range = toc.Range
            print(f"Table of contents found in '{doc.Name}'")
            return toc_range.End
    except Exception as e:
        print(f"Error identifying TOC in '{doc.Name}': {e}")
    return 0  # If no TOC is found, start from the beginning

def extract_section_content(doc, heading_texts, heading_styles_ordered, file_path):
    """
    Extracts content under headings that exactly match the specified texts in heading_texts,
    ignoring numbering and additional text, searching within the first 20 pages of the document.
    """
    content = ''
    try:
        print(f"Entering 'extract_section_content' for file '{file_path}', headings '{heading_texts}'")

        # Get the end position of the TOC
        toc_end = get_toc_end_position(doc)

        # Get the end position of page 20 or the end of the document if less than 20 pages
        try:
            page_20_range = doc.GoTo(What=1, Which=1, Count=20)  # wdGoToPage, wdGoToAbsolute
            end_page_20 = page_20_range.End
            print(f"End position of page 20 in '{file_path}': {end_page_20}")
        except Exception as e:
            print(f"Error getting end position of page 20 in '{file_path}': {e}")
            end_page_20 = doc.Content.End

        # Ensure the end position is after the TOC end
        if end_page_20 < toc_end:
            end_page_20 = doc.Content.End

        # Set the search range
        search_range = doc.Range(Start=toc_end, End=end_page_20)
        current_pos = search_range.Start

        # Normalize the heading texts for comparison
        normalized_heading_texts = [ht.lower() for ht in heading_texts]

        while current_pos < end_page_20:
            para_range = doc.Range(Start=current_pos, End=end_page_20)
            if para_range.Start >= para_range.End:
                break  # No more content
            para = para_range.Paragraphs(1)
            para_text = para.Range.Text.strip()
            para_style_name = para.Style.NameLocal

            # Check if paragraph is a heading
            if para_style_name in heading_styles_ordered:
                # Remove numbering from the heading text
                heading_text_no_number = re.sub(r'^\d+(\.\d+)*\s*', '', para_text).strip()
                heading_text_no_number_lower = heading_text_no_number.lower()

                if heading_text_no_number_lower in normalized_heading_texts:
                    print(f"Found heading '{para_text}' matching '{heading_texts}' in '{file_path}'")
                    # Get the starting position after the found heading
                    start_pos = para.Range.End
                    content_paras = []
                    current_content_pos = start_pos

                    while current_content_pos < end_page_20:
                        content_para_range = doc.Range(Start=current_content_pos, End=end_page_20)
                        if content_para_range.Start >= content_para_range.End:
                            break  # No more content
                        content_para = content_para_range.Paragraphs(1)
                        content_para_text = content_para.Range.Text.strip()
                        content_para_style_name = content_para.Style.NameLocal

                        # Check if paragraph is a heading
                        if content_para_style_name in heading_styles_ordered:
                            current_style_index = heading_styles_ordered.index(para_style_name)
                            next_style_index = heading_styles_ordered.index(content_para_style_name)
                            if next_style_index <= current_style_index:
                                # Reached a heading of same or higher level
                                print(f"Reached heading '{content_para_text}' with style '{content_para_style_name}' in '{file_path}', stopping content extraction.")
                                break

                        # Add paragraph to content
                        content_paras.append(content_para.Range.Text)
                        # Move to next paragraph
                        current_content_pos = content_para.Range.End

                    content = ''.join(content_paras).strip()
                    break  # Exit after finding the content

            # Move to next paragraph
            current_pos = para.Range.End

        if content:
            print(f"Extracted content for heading '{heading_texts}' in '{file_path}'")
        else:
            print(f"No content found for headings '{heading_texts}' in '{file_path}'")

    except pywintypes.com_error as e:
        print(f"COM error in 'extract_section_content' for '{file_path}': {e}")
    except Exception as e:
        print(f"Error in 'extract_section_content' for '{file_path}': {e}")
    finally:
        print(f"Exiting 'extract_section_content' for file '{file_path}', headings '{heading_texts}'")
    return content

# Define the heading styles to look for, ordered from highest to lowest level
heading_styles_ordered = ["Heading 1", "Heading 2", "Heading 3", "Titre 1", "Titre 2", "Titre 3"]

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.lower().endswith(('.doc', '.docx')):
            file_path = os.path.join(root, file)

            # Increment the file counter before processing
            file_count += 1

            print(f"\nProcessing file {file_count}: {file_path}")
            print(f"File name: {file}")

            try:
                print(f"Attempting to open document '{file_path}'")
                # Open the document in read-only mode
                doc = word.Documents.Open(file_path, ReadOnly=True)
                print(f"Successfully opened document '{file_path}'")
            except pywintypes.com_error as e:
                print(f"Error opening '{file_path}': {e}")
                skipped_files.append(file_path)
                continue
            except Exception as e:
                print(f"Unexpected error opening '{file_path}': {e}")
                skipped_files.append(file_path)
                continue

            # Initialize variables with default empty values
            file_name = os.path.basename(file_path)
            directory_path = os.path.dirname(file_path)
            size = ''
            pages = ''
            num_paragraphs = ''
            objective_content = ''
            scope_content = ''
            content_content = ''

            try:
                # Get the size of the document
                try:
                    size = os.path.getsize(file_path)
                    print(f"Size of '{file_path}': {size} bytes")
                except Exception as e:
                    print(f"Error getting size for '{file_path}': {e}")
                    size = ''

                # Get the total number of pages
                try:
                    pages = get_page_count(doc)
                    print(f"Total pages in '{file_path}': {pages}")
                except Exception as e:
                    print(f"Error getting page count for '{file_path}': {e}")
                    pages = ''

                # Get the number of paragraphs
                try:
                    num_paragraphs = get_paragraph_count(doc)
                    print(f"Number of paragraphs in '{file_path}': {num_paragraphs}")
                except Exception as e:
                    print(f"Error getting paragraph count for '{file_path}': {e}")
                    num_paragraphs = ''

                # Define the headings to search for each section
                headings_dict = {
                    'objective': ['Objectif', 'But du document', 'Purpose', 'OBJECTIF ET CONTEXTE'],
                    'scope': ['Périmètre'],
                    'content': ['Contenu', 'Content']
                }

                # Extract content for each section
                for section, heading_texts in headings_dict.items():
                    print(f"Extracting section '{section}' for '{file_path}'")
                    content = extract_section_content(doc, heading_texts, heading_styles_ordered, file_path)
                    if section == 'objective':
                        objective_content = content
                    elif section == 'scope':
                        scope_content = content
                    elif section == 'content':
                        content_content = content

                # Sanitize the extracted content
                objective_content = remove_illegal_characters(objective_content.strip())
                scope_content = remove_illegal_characters(scope_content.strip())
                content_content = remove_illegal_characters(content_content.strip())
                file_name = remove_illegal_characters(file_name)
                file_path = remove_illegal_characters(file_path)

                # Write the data to Excel
                ws.append([
                    file_name,
                    directory_path,
                    pages,
                    num_paragraphs,
                    size,
                    objective_content,
                    scope_content,
                    content_content
                ])
                print(f"Data written to Excel for '{file_name}'.")
            except Exception as e:
                print(f"Error processing '{file_path}': {e}")
                skipped_files.append(file_path)
            finally:
                # Ensure the document is closed
                try:
                    if doc is not None:
                        print(f"Attempting to close document '{file_path}'")
                        doc.Close(False)  # Close without saving
                        del doc
                        gc.collect()
                        print(f"Successfully closed document '{file_path}'")
                except Exception as e:
                    print(f"Error closing document '{file_path}': {e}")
                    word = initialize_word()

print(f"\nTotal files processed: {file_count}")

# Close the Word application
try:
    word.Quit()
    word = None  # Release the COM object
    gc.collect()
    print("Word application closed.")
except Exception as e:
    print(f"Error quitting Word application: {e}")

# Save the Excel workbook
try:
    wb.save('doc_output.xlsx')
    print("Excel workbook 'output.xlsx' saved successfully.")
except Exception as e:
    print(f"Error saving Excel workbook: {e}")

# Display the skipped files
if skipped_files:
    print("\nThe following files were skipped due to errors:")
    for f in skipped_files:
        print(f)
else:
    print("\nAll files were processed successfully.")
