#!/bin/bash

# Path to the CHANGELOG.md file
CHANGELOG_FILE="CHANGELOG.md"

# Check if the CHANGELOG.md file exists
if [ -f "$CHANGELOG_FILE" ]; then
    # Display the contents of the CHANGELOG.md file
    cat "$CHANGELOG_FILE"
else
    echo "Changelog not available."
fi
