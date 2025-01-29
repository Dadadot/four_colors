#!/bin/bash

# Source directory containing .ui files
COMMON_SUBDIR="src/four_colors/view"

SRC_DIR="${COMMON_SUBDIR}/ui_files/"

# Destination directory for compiled .py files
DEST_DIR="${COMMON_SUBDIR}/ui_compiled/"

# Ensure the destination directory exists
mkdir -p "$DEST_DIR"

# Loop through each .ui file in the source directory
for ui_file in "$SRC_DIR"*.ui; do
    # Extract the base name of the file (without path and extension)
    base_name=$(basename "$ui_file" .ui)
    
    # Compile the .ui file and save it in the destination directory
    pyside6-uic "$ui_file" -o "$DEST_DIR/${base_name}.py"
done

echo "UI files compiled successfully!"
