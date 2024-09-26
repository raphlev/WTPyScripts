import os

def get_unique_extensions(directory):
    # Set to store unique file extensions
    extensions = set()

    # Walk through all the subfolders and files in the given directory
    for root, _, files in os.walk(directory):
        for file in files:
            # Split the file extension and add it to the set
            ext = os.path.splitext(file)[1]
            if ext:
                extensions.add(ext.lower())  # Use lower case for consistency

    return extensions

if __name__ == "__main__":
    # Define the root directory to scan
    directory_to_scan = r'C:\Users\levequer\Downloads'  # Replace with the path you want to scan

    unique_extensions = get_unique_extensions(directory_to_scan)
    
    # Print the unique extensions found
    print("Unique file extensions found:")
    for ext in sorted(unique_extensions):
        print(ext)
