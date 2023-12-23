#!/bin/bash

# Specify the folder path
folder_path="/app/images/"

# Change to the specified folder
cd "$folder_path" || exit

# Delete files older than 5 minutes
find . -type f -mmin +5 -exec rm {} \;

# Optional: Print a message indicating the operation is complete
echo "Files older than 5 minutes deleted in $folder_path"
