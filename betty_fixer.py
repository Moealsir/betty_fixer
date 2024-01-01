import re
import sys
import os
import subprocess
from backup import *
from errors_extractor import *
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
    clean_errors_file('errors.txt')

    content = fix_comments(content)
    content = remove_trailing_whitespaces(content)

    # Return the file path for further processing
    return file_path

def remove_blank_lines_inside_comments(file_path):
    clean_errors_file('errors.txt')
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
        errors_file_path = 'errors.txt'
        functions_with_no_description = extract_functions_with_no_description(errors_file_path)

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
        fix_missing_blank_line_after_declarations(errors_file_path)
        remove_blank_lines_inside_comments(file_path)
        fix_should_be_void(errors_file_path)
        More_than_5_functions_in_the_file(errors_file_path)
        fix_brace_should_be_on_the_next_line(errors_file_path)
        fix_brace_should_be_on_the_previous_line(errors_file_path)
        content = read_file(file_path)
        content = remove_trailing_whitespaces(content)
        write_file(file_path, content)
        betty_handler(errors_file_path)



def More_than_5_functions_in_the_file(errors_file_path):
    # Set to True initially to enter the loop
    errors_fixed = True

    while errors_fixed:
        errors_fixed = False  # Reset the flag at the beginning of each iteration

        with open(errors_file_path, 'r') as errors_file:
            # Read all lines at once to allow modification of the list while iterating
            error_lines = errors_file.readlines()

            for error_line in error_lines:
                if 'More than 5 functions in the file' in error_line:
                    variables = extract_and_print_variables(error_line)
                    if len(variables) >= 2:
                        file_path, _ = variables[:2]
                        line_number = 1  # Assuming you want to start from the first line
                        with open(file_path, 'r') as file:
                            lines = file.readlines()

                        # Find the next available file name (file1.c, file2.c, etc.)
                        new_file_path = find_available_file_name(file_path)

                        # Count the /** ... */ blocks
                        counter = 0
                        inside_block = False
                        block_start_line = 0
                        for idx, line in enumerate(lines):
                            if line.strip().startswith('/**'):
                                inside_block = True
                                block_start_line = idx
                            elif inside_block and line.strip().startswith('*/'):
                                inside_block = False
                                counter += 1

                            if counter == 6:
                                # Create a new file with the content from the specified line to the end of the file
                                copy_remaining_lines(lines, block_start_line, new_file_path)
                                # Remove the content from the main file
                                del lines[block_start_line:]
                                # Write the modified content back to the main file
                                with open(file_path, 'w') as main_file:
                                    main_file.write(''.join(lines))
                                # Clean 'errors.txt' before extracting new errors
                                open(errors_file_path, 'w').close()
                                # Update Betty errors in errors.txt
                                exctract_errors(new_file_path, errors_file_path)
                                errors_fixed = True  # Set the flag if a line is fixed
                                break

                            line_number += 1

def find_available_file_name(original_file_path):
    base_name, extension = os.path.splitext(original_file_path)
    counter = 1

    while True:
        # Remove :01d from the format to allow for sequential numbering without leading zeros
        new_file_path = f'{base_name}{counter}{extension}'
        if not os.path.exists(new_file_path):
            return new_file_path
        counter += 1

def copy_remaining_lines(lines, start_line, new_file_path):
    # Create a new file with the content from the specified line to the end of the file
    with open(new_file_path, 'w') as new_file:
        new_file.write(''.join(lines[start_line:]))
        

def betty_handler(errors_file_path):
    with open(errors_file_path, 'r') as errors_file:
        # Read all lines at once to allow modification of the list while iterating
        error_lines = errors_file.readlines()

        messages = ["More than 40 lines in a function",
                    "line over 80 characters"
                    ]

        for error_line in error_lines:
            for message in messages:
                if message in error_line:
                    variables = extract_and_print_variables(error_line)
                    if len(variables) >= 1:
                        # Extract the first element from the tuple
                        file_path = variables[0]
                        other_handlers(file_path)

def other_handlers(file_path):
    errors_file_path = 'errors.txt'
    # Your logic code

    create_tasks_directory()
    # Pass file_path as a list to copy_files_to_tasks
    copy_files_to_tasks([file_path])
    modify_main_files([file_path])

    # Clean 'errors.txt' before extracting new errors
    clean_errors_file(errors_file_path)

    # Update Betty errors in errors.txt
    exctract_errors(file_path, errors_file_path)

def create_tasks_directory():
    # Create tasks directory if not found
    if not os.path.exists("tasks"):
        os.makedirs("tasks")

def copy_files_to_tasks(files):
    # Copy files to tasks directory
    for file_path in files:
        destination_path = os.path.join("tasks", os.path.basename(file_path))
        if not os.path.exists(destination_path):
            # Read the content of the file
            with open(file_path, 'r') as source_file:
                content = source_file.readlines()

            # Exclude lines starting with #include and ending with '.h"'
            filtered_content = [line for line in content if not line.strip().startswith("#include") or not line.strip().endswith('.h"')]

            # Write the modified content to the destination file
            with open(destination_path, 'w') as destination_file:
                destination_file.write(''.join(filtered_content))

def modify_main_files(files):
    # Modify main files
    for file_path in files:
        # Read the content of the main file
        with open(file_path, 'r') as main_file:
            content = main_file.readlines()

        # Keep only lines with #include that end with '.h"'
        include_lines = [line.strip() for line in content if line.strip().startswith("#include") and line.strip().endswith('.h"')]

        # Write the modified content to the main file, adding an empty line at the end
        with open(file_path, 'w') as main_file:
            main_file.write('\n'.join(include_lines + [f'#include "tasks/{os.path.basename(file_path)}"\n']))


        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python betty_fixer.py file1.c file2.c ...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    open('errors.txt', 'w').close()
    # Fix Betty style
    fix_betty_style(file_paths)
    for file in file_paths:
        run_vi_script(file)
    