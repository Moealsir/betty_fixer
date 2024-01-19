#!/bin/bash

# Check if Betty is installed
betty_executable=$(command -v betty)
if [ -z "$betty_executable" ]; then
    echo "Betty not found. Installing..."
    sudo ./bettyfixer/install_dependency/.Betty/install.sh
    sudo cp ./bettyfixer/install_dependency/.betty /bin/betty
fi

# Check if black is installed, if not install it
black_executable=$(command -v black)
if [ -z "$black_executable" ]; then
    echo "Black not found. Installing..."
    sudo pip install black
fi

# Check if exuberant-ctags is installed, if not install it
ctags_executable=$(command -v ctags)
if [ -z "$ctags_executable" ]; then
    echo "Exuberant-ctags not found. Installing..."
    sudo apt-get install exuberant-ctags
fi

# Run .install.sh in the current directory
./.install.sh
