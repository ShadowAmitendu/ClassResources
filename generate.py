import os
import json
from datetime import datetime

# --- CONFIGURATION ---
TARGET_FOLDERS = ["syllabus", "notes", "assignments"]
OUTPUT_FILE = "files.json"

def get_files_recursive(folder_path):
    structure = []
    try:
        # Sort items: Directories first, then files (case-insensitive)
        items = sorted(os.listdir(folder_path), key=lambda x: (not os.path.isdir(os.path.join(folder_path, x)), x.lower()))

        for item in items:
            full_path = os.path.join(folder_path, item)

            # Ignore hidden files (like .git, .DS_Store)
            if item.startswith('.'):
                continue

            if os.path.isdir(full_path):
                structure.append({
                    "type": "dir",
                    "name": item,
                    "path": full_path.replace("\\", "/"), # Fix for Windows paths
                    "children": get_files_recursive(full_path)
                })
            else:
                # Use RELATIVE path so it works on Localhost AND GitHub
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

# --- MAIN EXECUTION ---
print("🚀 Starting Generator...")
data = {}

# 1. Get Local Date (Solves the "2 Push" problem)
now = datetime.now().strftime("%B %d, %Y") # e.g., "January 25, 2026"
data["metadata"] = {
    "lastUpdated": now
}
print(f"📅 Date set to: {now}")

# 2. Scan Local Folders
for folder in TARGET_FOLDERS:
    if os.path.exists(folder):
        print(f"📂 Scanning {folder}...")
        data[folder] = get_files_recursive(folder)
    else:
        print(f"❌ Missing folder: {folder}")
        data[folder] = []

# 3. Save JSON
with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"✅ Done! Saved to {OUTPUT_FILE}")
print("👉 Now you can: git add . -> git commit -> git push")