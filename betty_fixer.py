import re
import sys
import os
import subprocess
from backup import *
from errors_extractor import exctract_errors
from extract_line import *


def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def add_line_without_newline(file_path, line):
    # Add a line without a newline at the end of the file if not found
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1] if lines else ''

    if not last_line.strip() == line.strip():
        with open(file_path, 'a') as file:
            file.write(line)
            
def remove_consecutive_blank_lines(content):
    # Remove multiple consecutive blank lines
    return re.sub('\n{3,}', '\n\n', content)

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

def process_errors(file_path):
    # Process the errors for the specified file
    errors_file_path = 'errors.txt'
    process_error_file(errors_file_path)

def fix_betty_warnings(content, file_path):
    # Run Betty and append errors to the common errors.txt file
    content = remove_consecutive_blank_lines(content)
    exctract_errors(file_path, 'errors.txt')

    content = fix_comments(content)
    content = remove_trailing_whitespaces(content)

    # Return the file path for further processing
    return file_path

def remove_blank_lines_inside_comments(file_path):
    exctract_errors(file_path, 'errors.txt')
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find lines starting with '/**' (declaration beginning)
    for i, line in enumerate(lines):
        if line.strip().startswith('/**'):
            # Find the next line starting with ' */' (declaration ending)
            for j in range(i + 1, len(lines)):
                if lines[j].strip().startswith('*/'):
                    # Remove any blank lines between declaration beginning and ending
                    for k in range(i + 1, j):
                        if lines[k].strip() == '':
                            del lines[k]

                    # Write the modified content back to the file
                    with open(file_path, 'w') as file:
                        file.writelines(lines)
                    return

def fix_betty_style(file_paths):
    for file_path in file_paths:
        create_backup(file_path)
        run_vi_script(file_path)
        content = read_file(file_path)
        content = fix_comments(content)
        content = add_parentheses_around_return(content)
        content = remove_trailing_whitespaces(content)
        content = remove_consecutive_blank_lines(content)
        file_path_with_errors = fix_betty_warnings(content, file_path)
        write_file(file_path, content)
        add_line_without_newline(file_path, '\n')

        for _ in range(2):
            process_errors(file_path_with_errors)

        # Extract functions with no description from 'errors.txt'
        functions_with_no_description = extract_functions_with_no_description('errors.txt')

        # Iterate through each line in path_file and remove extra spaces
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        cleaned_lines = [remove_extra_spaces(line) for line in lines]

        # Write the cleaned lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(cleaned_lines)

        # Generate documentation for each function with no description
        for function_name in functions_with_no_description:
            remove_unused_attribute(file_path, function_name)
        run_vi_script(file_path)

        # Fix missing blank line after declarations
        with open('errors.txt', 'r') as errors_file:
            for error_line in errors_file:
                if 'Missing a blank line after declarations' in error_line:
                    # Extract (file_path, line_number) from the error line
                    variables = extract_and_print_variables(error_line)
                    if len(variables) >= 2:
                        file_path, line_number = variables[:2]  # Take the first two values
                        # Fix missing blank line after declaration
                        fix_missing_blank_line_after_declaration(file_path, line_number)

                        # Update Betty errors in errors.txt and restart searching
                        exctract_errors(file_path, 'errors.txt')
                        
        remove_blank_lines_inside_comments(file_path)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python betty_fixer.py file1.c file2.c ...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    open('errors.txt', 'w').close()
    # Fix Betty style
    fix_betty_style(file_paths)