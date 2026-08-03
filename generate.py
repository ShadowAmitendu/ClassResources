#!/usr/bin/env python3
"""
File Index Generator for Class Resources Website
================================================

This script scans specified directories (syllabus, notes, assignments) and
generates a JSON file (files.json) containing metadata about all files and folders.
The generated JSON is consumed by index.html to dynamically render the file listing.

Usage:
    python generate.py

Output:
    files.json - Contains file structure and metadata for each section

Author: Amitendu Bikash Dhusiya
Project: Class Resources - BCA 6th Semester
"""

import os
import json
from datetime import datetime

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# Define the folders to scan. These must match the SECTIONS array in index.html
TARGET_FOLDERS = ["syllabus", "notes", "assignments"]

# Output filenames for generated JSON
OUTPUT_FILE_7TH = "files.json"
SEM6_FOLDER = "6th_sem"
OUTPUT_FILE_6TH = "files_6th_sem.json"


def get_files_recursive(folder_path):
    """
    Recursively scans a directory and returns its structure as a list.

    This function traverses the given folder and creates a hierarchical structure
    representing all files and subdirectories. Directories are listed first,
    followed by files, both sorted alphabetically (case-insensitive).

    Args:
        folder_path (str): The path to the directory to scan.

    Returns:
        list: A list of dictionaries, where each dictionary represents either:
            - A file: {"type": "file", "name": str, "path": str, "url": str}
            - A directory: {"type": "dir", "name": str, "path": str, "children": list}
    """
    structure = []
    try:
        # Sort items: Directories first, then files (case-insensitive alphabetical)
        items = sorted(
            os.listdir(folder_path),
            key=lambda x: (not os.path.isdir(os.path.join(folder_path, x)), x.lower())
        )

        for item in items:
            full_path = os.path.join(folder_path, item)

            # Skip hidden files and system files (e.g., .git, .DS_Store, Thumbs.db)
            if item.startswith('.'):
                continue

            if os.path.isdir(full_path):
                # Add directory entry with recursive children
                structure.append({
                    "type": "dir",
                    "name": item,
                    "path": full_path.replace("\\", "/"),  # Normalize Windows paths to Unix style
                    "children": get_files_recursive(full_path)
                })
            else:
                # Add file entry with relative path for cross-platform compatibility
                relative_path = full_path.replace("\\", "/")
                structure.append({
                    "type": "file",
                    "name": item,
                    "path": relative_path,
                    "url": relative_path
                })

    except FileNotFoundError:
        print(f"⚠️ Warning: Folder '{folder_path}' not found. Skipping.")

    return structure


def generate_json_for(base_dir, output_file, is_subfolder=False):
    """
    Scans target folders in base_dir and writes the metadata dictionary to output_file.
    """
    data = {}
    now = datetime.now().strftime("%B %d, %Y")
    data["metadata"] = {
        "lastUpdated": now
    }

    for folder in TARGET_FOLDERS:
        folder_path = os.path.join(base_dir, folder) if is_subfolder else folder
        if os.path.exists(folder_path):
            print(f"📂 Scanning '{folder_path}' folder...")
            data[folder] = get_files_recursive(folder_path)
        else:
            print(f"❌ Missing folder: '{folder_path}' - Creating empty entry")
            data[folder] = []

    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Successfully generated '{output_file}'")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("🚀 Starting File Index Generator...")

    print("\n--- 7th Semester (Current) ---")
    generate_json_for(".", OUTPUT_FILE_7TH, is_subfolder=False)

    print("\n--- 6th Semester (Completed) ---")
    if os.path.exists(SEM6_FOLDER):
        generate_json_for(SEM6_FOLDER, OUTPUT_FILE_6TH, is_subfolder=True)
    else:
        print(f"⚠️ Warning: '{SEM6_FOLDER}' directory not found. Skipping 6th Sem index.")

    print("\n👉 Next steps: git add . → git commit -m 'Update files' → git push")

