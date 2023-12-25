import re
import sys
import os
import subprocess
from backup import *
from spaces import *
from errors_extractor import run_betty

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def add_parentheses_around_return(content):
    # Add parentheses around return values if not already present
    content = re.sub(r'return[ ]+([^(][^;]+);', r'return (\1);', content)

    # Add parentheses around return values if no value is present and not already in parentheses
    content = re.sub(r'return[ ]+([^;()]+);', r'return (\1);', content)

    # Check if space after semicolon before closing brace '}' is needed
    if not re.search(r';\s*}', content):
        # Add space after semicolon before closing brace '}'
        content = re.sub(r';}', r';\n}', content)

    return content

def fix_comments(content):
    # Remove single-line comments (//) found alone in a line or after a code line
    return re.sub(r'([^;])\s*//.*|^\s*//.*', r'\1', content, flags=re.MULTILINE)

def remove_trailing_whitespaces(content):
    # Remove trailing whitespaces at the end of lines
    return re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

def run_vi_script(filename):
    # Specify the file you want to edit
    filename = os.path.abspath(filename)
    # Run the vi command with gg=G using the -c option
    subprocess.run(['vi', '-c', 'normal! gg=G', '-c', 'wq', filename])


def fix_betty_warnings(content, file_path):
    # Run Betty and append errors to the common errors.txt file
    content = remove_consecutive_blank_lines(content)
    run_betty(file_path, 'errors.txt')

    content = fix_comments(content)
    content = remove_trailing_whitespaces(content)
    content = add_parentheses_around_return(content)

    return content

def fix_betty_style(file_paths):
    for file_path in file_paths:
        create_backup(file_path)  # Create a backup before making changes

        # Run the vi script for each file
        run_vi_script(file_path)

        # Read file content
        content = read_file(file_path)

        # Apply fixes for warnings and write errors to the file
        content = fix_betty_warnings(content, file_path)

        # Write the fixed content back to the file
        write_file(file_path, content)

        # Add a line without a newline at the end of the file
        add_line_without_newline(file_path, '\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python betty_fixer.py file1.c file2.c ...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    open('errors.txt', 'w').close()
    # Fix Betty style
    fix_betty_style(file_paths)
