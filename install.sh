#!/bin/bash

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