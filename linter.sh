#!/bin/env bash

# Get the current date and time
CURRENT_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Get the name of the person from git config
NAME=$(git config --get user.name)

# path from the root of project to the directory where the log files will be saved
PATHLOG=$(git rev-parse --show-toplevel)/error_logs/linting
# Check if pylint is installed
if ! command -v pylint &> /dev/null
then
    echo "pylint is not installed"
    exit 1
fi

# Check if person's name is set in git config
if [ -z "$(git config --get user.name)" ]
then
    echo "Please set your name in git config"
    exit 1
fi


if [ ! -d "$PATHLOG" ]
then
    mkdir -p "$PATHLOG"
fi
# Loop over all command line arguments
for file in "$@"
do
    # Change the file suffix to .txt
    output_file="${file%.py}.txt"


    echo -e "\n\nName: $NAME\n" >> "${PATHLOG}/${output_file}"
    echo -e "Date: $CURRENT_DATE\n" >> "${PATHLOG}/${output_file}"
    pylint "$file" 
    # Run pylint with the current command line argument
    pylint "$file" --reports=y -f parseable >> "${PATHLOG}/${output_file}"
done