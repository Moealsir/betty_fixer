#!/bin/bash

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "\e[1;31mPlease run with sudo:
    sudo ./install.sh\e[0m"
    exit 1
fi

# Check if betty is installed, if not, install it
if ! command -v betty &> /dev/null; then
    # Clone the repo to your local machine
    git clone https://github.com/alx-tools/Betty.git
    # cd into the Betty directory
    cd Betty
    # Install the linter with sudo ./install.sh
    (sudo ./install.sh &)
    # Go back to the main dir
    cd ..
    # Run sudo cp betty /bin/
    sudo cp Betty/betty /bin/
fi


# Clear the terminal
clear 

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    # Install python3 if not installed
    sudo apt-get update
    sudo apt-get install -y python3
fi

# Copy fixer into bin
cp -r fixer/ /bin/

# # Add an alias to .bashrc
echo "alias fix='python3 /bin/fixer/betty_fixer.py'" >> ~/.bashrc

# Clear the terminal
clear 

# Inform the user about the changes
echo -e "Please copy and run this command:\n"
echo -e "    \e[1;33msource ~/.bashrc\e[0m\n"
read -p "Press [Enter] key to continue ..."

clear

echo -e "\e[1;33mUsage:\e[0m\n"
echo -e "    fix file1.c file2.c ....\n"
read -p "Press [Enter] key to continue ..."

clear 

# Display a warning message
echo "#############################################################"
echo -e "#                        \e[1;33mWARNING\e[0m                            #"
echo "#   This program will overwrite your files.                 #"
echo "#   But ...                                                 #"
echo "#   It will create a backup file. If you run the program    #
#   twice, you will lose your original code.                #"
echo "#############################################################"

# Ensure the user has read the warning
read -p "Press [Enter] key to continue ..."

clear
echo -e "\n\e[1;35m###########################################################\e[0m"
echo -e "\e[1;32m       Program Successfully Installed and Ready to Go!\e[0m\n"
echo -e "            \e[1;36mCoded by: Moealsir && malazmuzamil\e[0m"
echo -e "  Thank you for choosing this Fixer. "
echo -e "                               \e[1;34mEnjoy your experience!!\e[0m"
echo -e "\e[1;35m###########################################################\e[0m\n"