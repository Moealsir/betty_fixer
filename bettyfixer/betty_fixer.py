"""Betty Fixer main module."""
import re
import sys
import os
from bettyfixer.backup import create_backup
from bettyfixer.errors_extractor import exctract_errors
from bettyfixer.extract_line import (
    process_error_file,
    clean_errors_file,
    run_vi_script,
    extract_functions_with_no_description,
    remove_extra_spaces,
    remove_unused_attribute,
    fix_missing_blank_line_after_declarations,
    fix_should_be_void,
    fix_brace_should_be_on_the_next_line,
    fix_brace_should_be_on_the_previous_line,
    extract_and_print_variables
)
from bettyfixer.autoprototype import (
    betty_check,
    print_check_betty_first,
    print_header_name_missing,
    autoproto
)

HIDDEN_FILE_NAME = ".processed_files"


def read_file(file_path):
    """
    Read the content of the specified file.
    Args:
        file_path (str): The path of the file to read.
    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def write_file(file_path, content):
    """
    Write the specified content to the specified file.
    Args:
        file_path (str): The path of the file to write to.
        content (str): The content to write to the file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def add_line_without_newline(file_path, line):
    """
    Add a line without a newline at the end of the file if not found.
    Args:
        file_path (str): The path of the file to add the line to.
        line (str): The line to add to the file.
    """
    # Add a line without a newline at the end of the file if not found
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        last_line = lines[-1] if lines else ''

    if not last_line.strip() == line.strip():
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(line)


def remove_consecutive_blank_lines(content):
    """
    Remove multiple consecutive blank lines from the specified content.
    Args:
        content (str):
            The content to remove multiple consecutive blank lines from.
    Returns:
        str: The content with multiple consecutive blank lines removed.
    """
    # Remove multiple consecutive blank lines
    return re.sub('\n{3,}', '\n\n', content)


def add_parentheses_around_return(content):
    """
    Add parentheses around return values if not already present.
    Args:
        content (str): The content to add parentheses around return values to.
    Returns:
        str: The content with parentheses around return values added.
    """
    # Add parentheses around return values if not already present
    content = re.sub(r'return[ ]+([^(][^;]+);', r'return (\1);', content)

    # Add parentheses around return values if no value
    # is present and not already in parentheses
    content = re.sub(r'return[ ]+([^;()]+);', r'return (\1);', content)

    # Check if space after semicolon before closing brace '}' is needed
    if not re.search(r';\s*}', content):
        # Add space after semicolon before closing brace '}'
        content = re.sub(r';}', r';\n}', content)

    return content


def fix_comments(content):
    """
    Fix comments in the specified content.
    Args:
        content (str): The content to fix comments in.
    Returns:
        str: The content with comments fixed.
    """
    # Remove single-line comments (//) found alone in line or after a code line
    return re.sub(
        r'([^;])\s*//.*|^\s*//.*', r'\1', content, flags=re.MULTILINE)


def remove_trailing_whitespaces(content):
    """
    Remove trailing whitespaces at the end of lines in the specified content.
    Args:
        content (str): The content to remove trailing whitespaces from.
    Returns:
        str: The content with trailing whitespaces removed.
    """
    # Remove trailing whitespaces at the end of lines
    return re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)


# ❗ This function doesn't make sense to me [Younis]
def process_errors(file_path):
    """
    Process the errors for the specified file.
    Args:
        file_path (str): The path of the file to process the errors for.
    """
    # Process the errors for the specified file
    file_path = 'errors.txt'
    process_error_file(file_path)


def fix_betty_warnings(content, file_path):
    """
    Fix Betty warnings in the specified content.
    Args:
        content (str): The content to fix Betty warnings in.
        file_path (str): The path of the file to fix Betty warnings in.
    Returns:
        str: The file path for further processing.
    """
    # Run Betty and append errors to the common errors.txt file
    content = remove_consecutive_blank_lines(content)
    clean_errors_file('errors.txt')

    content = fix_comments(content)
    content = remove_trailing_whitespaces(content)

    # Return the file path for further processing
    return file_path


def remove_blank_lines_inside_comments(file_path):
    """
    Remove blank lines inside comments in the specified file.
    Args:
        file_path (str):
            The path of the file to remove blank lines inside comments from.
    """
    clean_errors_file('errors.txt')
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find lines starting with '/**' (declaration beginning)
    for i, line in enumerate(lines):
        if line.strip().startswith('/**'):
            # Find the next line starting with ' */' (declaration ending)
            for j in range(i + 1, len(lines)):
                if lines[j].strip().startswith('*/'):
                    # Remove any blank line <- declaration beginning and ending
                    for k in range(i + 1, j):
                        if lines[k].strip() == '':
                            del lines[k]

                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.writelines(lines)
                    return


def fix_betty_style(file_paths):
    """
    Fix Betty style for the specified file paths.
    Args:
        file_paths (list): The list of file paths to fix Betty style for.
    """
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
        functions_with_no_description = extract_functions_with_no_description(
            errors_file_path)

        # Iterate through each line in path_file and remove extra spaces
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        cleaned_lines = [remove_extra_spaces(line) for line in lines]

        # Write the cleaned lines back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(cleaned_lines)

        # Generate documentation for each function with no description
        for function_name in functions_with_no_description:
            remove_unused_attribute(file_path, function_name)
        run_vi_script(file_path)
        fix_missing_blank_line_after_declarations(errors_file_path)
        remove_blank_lines_inside_comments(file_path)
        fix_should_be_void(errors_file_path)
        more_than_5_functions_in_the_file(errors_file_path)
        fix_brace_should_be_on_the_next_line(errors_file_path)
        fix_brace_should_be_on_the_previous_line(errors_file_path)
        content = read_file(file_path)
        content = remove_trailing_whitespaces(content)
        write_file(file_path, content)
        betty_handler(errors_file_path)


def more_than_5_functions_in_the_file(errors_file_path):
    """
    Fix the error 'More than 5 functions in the file' in the specified file.
    Args:
        errors_file_path (str):
            The path of the errors file to fix the error in.
    """
    # Set to True initially to enter the loop
    errors_fixed = True

    while errors_fixed:
        errors_fixed = False  # Reset flag at the beginning of each iteration

        with open(errors_file_path, 'r', encoding='utf-8') as errors_file:
            # Read all lines at once to allow
            # modification of the list while iterating
            error_lines = errors_file.readlines()

            for error_line in error_lines:
                if 'More than 5 functions in the file' in error_line:
                    variables = extract_and_print_variables(error_line)
                    if len(variables) >= 2:
                        file_path, _ = variables[:2]
                        line_number = 1  # Assume to start from the first line
                        with open(file_path, 'r', encoding='utf-8') as file:
                            lines = file.readlines()

                        # Find the next avail file name (file1.c, file2.c, ..)
                        new_file_path = find_available_file_name(file_path)

                        # Count the /** ... */ blocks
                        counter = 0
                        in_block = False
                        block_start_line = 0
                        for idx, line in enumerate(lines):
                            if line.strip().startswith('/**'):
                                in_block = True
                                block_start_line = idx
                            elif in_block and line.strip().startswith('*/'):
                                in_block = False
                                counter += 1

                            if counter == 6:
                                # Create a new file with the content
                                # from the specified line to end of the file
                                copy_remaining_lines(
                                    lines, block_start_line, new_file_path)
                                # Remove the content from the main file
                                del lines[block_start_line:]
                                # Write the modified content back to main file
                                with open(
                                        file_path,
                                        'w',
                                        encoding='utf-8'
                                ) as main_file:
                                    main_file.write(''.join(lines))
                                # Clean 'errors.txt' before
                                    # extracting new errors
                                open(errors_file_path, 'w',
                                     encoding='utf-8').close()
                                # Update Betty errors in errors.txt
                                exctract_errors(
                                    new_file_path, errors_file_path)
                                # Set the flag if line is fixed
                                errors_fixed = True
                                break

                            line_number += 1


def find_available_file_name(original_file_path):
    """
    Find the next available file name based on the specified file path.
    Args:
        original_file_path (str):
            The path of the original file to find
                the next available file name for.
    Returns:
        str: The next available file name based on the original file path.
    """
    base_name, extension = os.path.splitext(original_file_path)
    counter = 1

    while True:
        # Remove :01d from the format to allow for sequential numbering without leading zeros
        new_file_path = f'{base_name}{counter}{extension}'
        if not os.path.exists(new_file_path):
            return new_file_path
        counter += 1


def copy_remaining_lines(lines, start_line, new_file_path):
    """
    Copy the remaining lines from the specified start line to the new file.
    Args:
        lines (list): The list of lines to copy from.
        start_line (int): The line number to start copying from.
        new_file_path (str): The path of the new file to copy the lines to.
    """
    # Create a new file with the content from the specified line to the end of the file
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(''.join(lines[start_line:]))


def betty_handler(errors_file_path):
    """
    Handle Betty errors in the specified file.
    Args:
        errors_file_path (str): The path of the errors file to handle Betty errors in.
    """
    with open(errors_file_path, 'r', encoding='utf-8') as errors_file:
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
    """
    Handle other errors in the specified file.
    Args:
        file_path (str): The path of the file to handle other errors in.
    """
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
    """
    Create the tasks directory if not found.
    """
    # Create tasks directory if not found
    if not os.path.exists("tasks"):
        os.makedirs("tasks")


def copy_files_to_tasks(files):
    """
    Copy the specified files to the tasks directory.
    Args:
        files (list): The list of files to copy to the tasks directory.
    """
    # Copy files to tasks directory
    for file_path in files:
        destination_path = os.path.join("tasks", os.path.basename(file_path))
        if not os.path.exists(destination_path):
            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as source_file:
                content = source_file.readlines()

            # Exclude lines starting with #include and ending with '.h"'
            filtered_content = [line for line in content if not line.strip(
            ).startswith("#include") or not line.strip().endswith('.h"')]

            # Write the modified content to the destination file
            with open(destination_path, 'w', encoding='utf-8') as destination_file:
                destination_file.write(''.join(filtered_content))


def modify_main_files(files):
    """
    Modify the main files to include the specified files.
    Args:
        files (list): The list of files to include in the main files.
    """
    # Modify main files
    for file_path in files:
        # Read the content of the main file
        with open(file_path, 'r', encoding='utf-8') as main_file:
            content = main_file.readlines()

        # Keep only lines with #include that end with '.h"'
        include_lines = [line.strip() for line in content if line.strip(
        ).startswith("#include") and line.strip().endswith('.h"')]

        # Write the modified content to the main file, adding an empty line at the end
        with open(file_path, 'w', encoding='utf-8') as main_file:
            main_file.write('\n'.join(
                include_lines + [f'#include "tasks/{os.path.basename(file_path)}"\n']))


def record_processed_file(filename):
    """
    Record the specified file as processed.
    Args:
        filename (str): The name of the file to record as processed.
    """
    with open(HIDDEN_FILE_NAME, 'a', encoding='utf-8') as hidden_file:
        hidden_file.write(filename + '\n')


def is_file_processed(filename):
    """
    Check if the specified file has been processed before.
    Args:
        filename (str): The name of the file to check if processed.
    Returns:
        bool: True if the file has been processed before, False otherwise.
    """
    if not os.path.exists(HIDDEN_FILE_NAME):
        return False

    with open(HIDDEN_FILE_NAME, 'r', encoding='utf-8') as hidden_file:
        processed_files = hidden_file.read().splitlines()
        return filename in processed_files


def main():
    """
    Main function for the Betty Fixer module.
    """
    if is_file_processed(".processed_files"):
        print("The files have already been processed. Skipping.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python -m betty_fixer_package.betty_fixer file1.c file2.c ...")
        sys.exit(1)

    if "-H" in sys.argv and len(sys.argv) > 2:

        if not betty_check():
            print_check_betty_first()
        else:
            header = sys.argv[sys.argv.index("-H") + 1]
            autoproto(".", header)
    elif "-H" in sys.argv and len(sys.argv) <= 2:
        print_header_name_missing()
    else:
        file_paths = sys.argv[1:]

        # Check if any file has been processed before
        if any(is_file_processed(file) for file in file_paths):
            print("One or more files have already been processed. Skipping.")
            sys.exit(1)

        open('errors.txt', 'w', encoding='utf-8').close()
        # Fix Betty style
        fix_betty_style(file_paths)
        for file in file_paths:
            run_vi_script(file)
            # Record processed file after completion
            record_processed_file(file)

        # Delete errors.txt file
        os.remove('errors.txt')


if __name__ == "__main__":
    main()
