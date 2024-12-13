import os
import re

# Function to generate renaming map based on the rules
# python.exe .\folders_rename.py
# Enter the parent folder path: C:\Users\levequer\TRANSITION TECHNOLOGIES PSC S.A\Project Space - Safran AE - Upgrade & Merge of Indigo & Opale Windchill 13\Technical space\02-Cadrage

def generate_rename_map(parent_folder):
    rename_map = {}

    # List all subfolders in the parent folder
    subfolders = [d for d in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, d))]

    # Filter subfolders with the prefix 10- and above
    prefix_pattern = re.compile(r'^(\d+)-')
    
    for folder in subfolders:
        match = prefix_pattern.match(folder)
        if match:
            prefix = int(match.group(1))
            if prefix >= 10:
                rename_map[folder] = f"{prefix + 1}-{folder[len(match.group(1)) + 1:]}"

    return dict(sorted(rename_map.items(), key=lambda x: int(re.match(prefix_pattern, x[0]).group(1)), reverse=True))

# Function to apply renaming with confirmation
def rename_folders(parent_folder, rename_map):
    print("Proposed renaming:")
    for old_name, new_name in rename_map.items():
        print(f"{old_name} -> {new_name}")

    confirmation = input("Do you want to proceed with renaming? (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Renaming aborted.")
        return

    # Perform renaming starting from the highest prefix
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(parent_folder, old_name)
        new_path = os.path.join(parent_folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")

if __name__ == "__main__":
    parent_folder = input("Enter the parent folder path: ").strip()

    # Convert input to a valid Windows path
    parent_folder = parent_folder.replace("\\", "/") if not parent_folder.startswith("r") else parent_folder

    if not os.path.isdir(parent_folder):
        print("Invalid folder path. Please check and try again.")
    else:
        rename_map = generate_rename_map(parent_folder)
        if rename_map:
            rename_folders(parent_folder, rename_map)
        else:
            print("No folders found to rename.")
