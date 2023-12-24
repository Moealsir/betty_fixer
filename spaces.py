import re

def add_line_without_newline(file_path, line):
    # Add a line without a newline at the end of the file if not found
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1] if lines else ''

    if not last_line.strip() == line.strip():
        with open(file_path, 'a') as file:
            file.write(line)
            
