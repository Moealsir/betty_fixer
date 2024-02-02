"""
This module contains functions for handling Betty style tasks.

The module can be run as a script, taking a list of file paths as command-line arguments.
When run as a script, it creates a tasks directory if one doesn't exist,
copies the specified files to the tasks directory, and modifies the main files.
"""
import os
import sys


def other_handler(file_path):
    """
    This function creates a tasks directory if one doesn't exist,
    copies the specified files to the tasks directory, and modifies the main files.
    """
    create_tasks_directory()
    copy_files_to_tasks(file_path)
    modify_main_files(file_path)


def create_tasks_directory():
    """
    Create a tasks directory if one doesn't exist.
    """
    # Create tasks directory if not found
    if not os.path.exists("tasks"):
        os.makedirs("tasks")


def copy_files_to_tasks(files):
    """
    Copy the specified files to the tasks directory.
    Args:
        files (list): A list of file paths to copy to the tasks directory.
    """
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
    Modify the main files to include the tasks.
    Args:
        files (list): A list of file paths to modify.

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


if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 2:
        print("Usage: python betty_handler.py file1.c file2.c ...")
        sys.exit(1)

    # Create tasks directory if not found
    create_tasks_directory()

    # Copy files to tasks directory if not found
    copy_files_to_tasks(sys.argv[1:])

    # Modify main files
    modify_main_files(sys.argv[1:])

    print("Tasks directory and main files modified successfully.")
