#!/bin/bash

# Specify the folder path
folder_path="/app/images/"

# Change to the specified folder
cd "$folder_path" || exit

# Delete files older than 2 days
find . -type f -mtime +2 -exec rm {} \;

# Optional: Print a message indicating the operation is complete
echo "Files older than 2 days deleted in $folder_path"
