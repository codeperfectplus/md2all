#!/bin/bash

# Backup original requirements.txt
cp requirements.txt requirements_backup.txt

# Empty the file to rewrite it with versions
> requirements.txt

# Loop through each package in the original file
while IFS= read -r package; do
  # Skip empty lines and comments
  if [[ -z "$package" || "$package" == \#* ]]; then
    echo "$package" >> requirements.txt
    continue
  fi

  # Get the installed version
  version=$(pip show "$package" 2>/dev/null | grep ^Version | awk '{print $2}')

  if [ -n "$version" ]; then
    echo "$package==$version" >> requirements.txt
  else
    echo "# $package not installed" >> requirements.txt
  fi
done < requirements_backup.txt
