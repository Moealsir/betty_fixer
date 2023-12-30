#!/bin/bash

# Clear the terminal
clear

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    # Install python3 if not installed
    sudo apt-get update
    sudo apt-get install -y python3
fi

# Copy directory into bin
sudo cp -r fixer /bin/

# Add an alias to .bashrc
echo "alias fix='python3 /bin/fixer/betty_fixer.py'" >> ~/.bashrc

# Reload .bashrc to apply changes
source ~/.bashrc

# Inform the user about the changes
echo -e "Please copy and run this command\n"
echo -e "       source ~/.bashrc \n\nin your terminal to apply changes."
read -p "Press [Enter] key to continue..."
