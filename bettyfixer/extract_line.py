"""
Extracts errors from the errors.txt file and fixes them in the specified file
"""
import re
import sys
import os
import subprocess
from bettyfixer.errors_extractor import exctract_errors


def run_vi_script(filename):
    """
    Run the vi command with gg=G using the -c option.
    Args:
        filename (str): The path of the file to edit.
    """
    # Specify the file you want to edit
    filename = os.path.abspath(filename)
    # Run the vi command with gg=G using the -c option
    try:
        # if it fails, check=True raise an exception
        subprocess.run(['vi', '-c', 'normal! gg=G',
                       '-c', 'wq', filename], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running vi: {e}")


def remove_extra_spaces(input_text):
    """
    Remove extra spaces from the input text.
    Args:
        input_text (str): The input text to remove extra spaces from.
    Returns:
        str: The input text with extra spaces removed.
    """
    lines = input_text.split('\n')
    cleaned_lines = []

    for line in lines:
        cleaned_line = ' '.join(line.split())
        cleaned_lines.append(cleaned_line)

    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text


def process_error_file(error_file_path):
    """
    Process the errors from the errors.txt file.
    Args:
        error_file_path (str): The path of the errors.txt file.
    """
    with open(error_file_path, 'r', encoding='utf-8') as errors_file:
        for error_line in errors_file:
            variables = extract_and_print_variables(error_line)
            if variables:
                file_path, line_number, error_description = variables
                fix_errors_from_file(file_path, line_number, error_description)


def extract_and_print_variables(error_line):
    """
    Extract and print variables from the error line.
    Args:
        error_line (str): The error line to extract variables from.
    Returns:
        tuple: A tuple containing the file path, line number,
        and error description.
    """

    # Split the error line to extract variables
    parts = error_line.split(":")
    if len(parts) >= 3:
        # Extracting file path and line number
        file_path, line_number, *error_parts = parts
        # Join all parts except the file path and line number
        # to get the error description
        error_description = ":".join(error_parts[1:]).strip()

        # Further processing if needed
        return file_path.strip(), line_number.strip(), error_description
    return None


def clean_up_line(line):
    """
    Remove extra spaces and ensure a single space before and after each word.
    Args:
        line (str): The line to clean up.
    Returns:
        str: The cleaned up line.
    """
    # Remove extra spaces and ensure a single space before and after each word
    cleaned_line = ' '.join(part.strip() for part in line.split(' '))

    # Add newline character if the original line had it
    if line.endswith('\n'):
        cleaned_line += '\n'

    return cleaned_line


def fix_errors_from_file(file_path, line_number, error_description):
    """
    Fix errors in the specified file.
    Args:
        file_path (str): The path of the file to fix errors in.
        line_number (str): The line number of the error.
        error_description (str): The description of the error.
    """
    # List of error messages
    error_messages = [
        "space prohibited between function name and open parenthesis",
        "space prohibited after that open parenthesis",
        "space prohibited before that close parenthesis",
        "space required before the open parenthesis",
        "space prohibited before semicolon",
        "should be \"foo *bar\"",
        "spaces prohibited around that '",
        "space prohibited after that '",
        "space prohibited before that '",
        "spaces preferred around that '",
        "space required after that '",
        "spaces required around that ",
        "space required before the open brace",
        "space required after that close brac",
        "should be \"foo **bar\"",
        "Statements should start on a tabstop",
    ]

    # Check each error message
    for i, message in enumerate(error_messages):
        if message in error_description:
            if i == 0:
                fix_space_between_func_name_open_parenthesis(
                    file_path, line_number, error_description)
            elif i == 1:
                fix_space_after_that_open_parenthesis(
                    file_path, line_number, error_description)
            elif i == 2:
                fix_space_before_that_close_parenthesis(
                    file_path, line_number, error_description)
            elif i == 3:
                fix_space_required_before_open_parenthesis(
                    file_path, line_number, error_description)
            elif i == 4:
                fix_space_prohibited_before_semicolon(
                    file_path, line_number, ';')
            elif i == 5:
                fix_should_be_foo_star_bar(
                    file_path, line_number, error_description)
            elif i == 6:
                fix_spaces_prohibited_around_that(
                    file_path, line_number, error_description)
            elif i == 7:
                fix_space_prohibited_after_that(
                    file_path, line_number, error_description)
            elif i == 8:
                fix_space_prohibited_before_that(
                    file_path, line_number, error_description)
            elif i == 9:
                fix_spaces_preferred_around_that(
                    file_path, line_number, error_description)
            elif i == 10:
                fix_space_required_after_that(
                    file_path, line_number, error_description)
            elif i == 11:
                fix_space_required_around_that(
                    file_path, line_number, error_description)
            elif i == 12:
                fix_space_required_before_the_open_brace(
                    file_path, line_number, error_description)
            elif i == 13:
                fix_space_required_after_the_close_brace(
                    file_path, line_number, error_description)
            elif i == 14:
                fix_should_be_foo_star_star_bar(
                    file_path, line_number, error_description)
            elif i == 15:
                run_vi_script(file_path)


def fix_should_be_void(error_file_path):
    """
    Fix errors in the specified file.
    Args:
        error_file_path (str): The path of the file to fix errors in.
    """
    errors_fixed = True  # Set to True initially to enter the loop

    while errors_fixed:
        errors_fixed = False  # Resets flag at the beginning of each iteration

        with open(error_file_path, 'r', encoding='utf-8') as errors_file:
            # Read all lines at once to allow modification
            # of the list while iterating
            error_lines = errors_file.readlines()

            for err_line in error_lines:
                if 'should probably be' in err_line and '(void)' in err_line:
                    # Extract (file_path, line_number) from the err line
                    variables = extract_and_print_variables(err_line)
                    if len(variables) >= 2:
                        # Take the first two values
                        file_path, line_num = variables[:2]

                        # Fix missing blank line after declaration
                        if should_be_void(file_path, line_num, 'errors.txt'):
                            errors_fixed = True  # Set flag if line is fixed


def should_be_void(file_path, line_number, error_file_path):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        error_file_path (str): The path of the errors.txt file.
    Returns:
        bool: True if the line is fixed, False otherwise.
    """
    # Convert line_number to integer
    line_number = int(line_number)
    specifier = '()'
    replacement = '(void)'

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Replace '()' with '(void)' in the specified line
    lines[line_number - 1] = lines[line_number -
                                   1].replace(specifier, replacement)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    # Clean 'errors.txt' before extracting new errors
    clean_errors_file(error_file_path)

    # Update Betty errors in errors.txt
    exctract_errors(file_path, error_file_path)

    return True  # Line is fixed, return True


def clean_errors_file(errors_file_path):
    """
    Clean the errors.txt file by removing its content.
    Args:
        errors_file_path (str): The path of the errors.txt file to clean.
    """
    errors_file_path = 'errors.txt'

    # Clear the content of the errors.txt file before appending new errors
    open(errors_file_path, 'w', encoding='utf-8').close()

    # Iterate over each file provided as a command-line argument
    for file_path in sys.argv[1:]:
        exctract_errors(file_path, errors_file_path)


def fix_missing_blank_line_after_declarations(errors_file_path):
    """
    Fix errors in the specified file.
    Args:
        errors_file_path (str): The path of the file to fix errors in.
    """
    errors_fixed = True  # Set to True initially to enter the loop

    while errors_fixed:
        errors_fixed = False  # Reset flag at the beginning of each iteration

        with open(errors_file_path, 'r', encoding='utf-8') as errors_file:
            # Read all lines at once to allow
            # modification of the list while iterating
            error_lines = errors_file.readlines()

            for error_line in error_lines:
                if 'Missing a blank line after declarations' in error_line:
                    # Extract (file_path, line_number) from the error line
                    variables = extract_and_print_variables(error_line)
                    if len(variables) >= 2:
                        # Take the first two values
                        fpath, line_num = variables[:2]

                        # Fix missing blank line after declaration
                        if fix_ln_after_declare(fpath, line_num, 'errors.txt'):
                            errors_fixed = True  # Setflag if line is fixed


def fix_ln_after_declare(file_path, line_number, errors_file_path):
    """
    Fix missing blank line after declaration.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        errors_file_path (str): The path of the errors.txt file.
    Returns:
        bool: True if the line is fixed, False otherwise.
    """
    # Convert line_number to integer
    line_number = int(line_number)

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    line_number -= 1
    # Check if a blank line is already present
    if lines[line_number].strip() == '':
        return False  # No fix needed, return False

    # Add a blank line after the specified line number
    lines.insert(int(line_number), '\n')

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    # Clean 'errors.txt' before extracting new errors
    clean_errors_file(errors_file_path)

    return True  # Line is fixed, return True


def fix_should_be_foo_star_star_bar(file_path, line_number, error_description):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        error_description (str): The description of the error.
    """
    # Specify the specifier
    specifier = '**'

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Check conditions and fix the line accordingly
    if 'foo** bar' in error_description:
        fixed_line = error_line.replace(f'{specifier} ', f' {specifier}')
    elif 'foo ** bar' in error_description:
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    elif 'foo**bar' in error_description:
        fixed_line = error_line.replace(f'{specifier}', f' {specifier}')
    elif 'foo* *bar' in error_description:
        fixed_line = error_line.replace('* *', f' {specifier}')
    else:
        # If none of the conditions match, return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def remove_unused_attribute(file_name, function_name):
    """
    Remove __attribute__((unused)) from the specified function in the file.
    Args:
        file_name (str): The path of the file to remove
            __attribute__((unused)) from.
        function_name (str): The name of the function to remove
            __attribute__((unused)) from.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Search for the function
        pattern = r'\b' + re.escape(function_name) + r'\b[^(]*\([^)]*\)'

        function_declarations = {}  # Dict to store function_name and its line

        for i, line in enumerate(lines):
            if re.search(pattern, line):
                fn_st_line = i  # function start line
                # Save the original line
                function_declarations[function_name] = lines[fn_st_line]
                break
        else:
            pass
        # took a copy from the original function declaration
        # original_declaration = lines[fn_st_line]# ❗ Unused variable [Younis]

        # Extract and remove __attribute__((unused))
        match = re.search(
            r'(__attribute__\s*\(\s*\(\s*unused\s*\)\s*\))', lines[fn_st_line])
        unused_attribute = match.group(1) if match else None
        lines[fn_st_line] = re.sub(
            r'__attribute__\s*\(\s*\(\s*unused\s*\)\s*\)',
            '',
            lines[fn_st_line])

        # Call the existing function to generate documentation
        generate_documentation(lines, fn_st_line, function_name)

        # Restore __attribute__((unused))
        if unused_attribute:
            lines[fn_st_line] = lines[fn_st_line].\
                replace(lines[fn_st_line].strip(
                ), lines[fn_st_line].strip() + ' ' + unused_attribute).strip()

        # Write back to the file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        fix_lines_in_file(file_name, function_declarations)
    except ValueError as e:
        print(f"ValueError: {e}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except OSError as e:
        print(f"OSError: {e}")


def fix_lines_in_file(file_name, function_declarations):
    """
    Fix the lines in the file.
    Args:
        file_name (str): The path of the file to fix the lines in.
        function_declarations (dict): A dictionary containing
            the function_name and its original line.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Iterate through each line in file
        for i, line in enumerate(lines):
            if '*/' in line and 'unused' in line:
                # Check if any function_name is found in this line
                for func_name, original_line in function_declarations.items():
                    if func_name in line:
                        # Replace the line with the desired format
                        lines[i] = f' */\n{original_line}'

                        # Check if the next line is a blank; if so, delete it
                        if i + 1 < len(lines) and lines[i + 1] == '\n':
                            del lines[i + 1]
                        break

        # Write back to the file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.writelines(lines)
    except ValueError as e:
        print(f"ValueError: {e}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except OSError as e:
        print(f"OSError: {e}")


def generate_documentation(lines, fn_start_ln, function_name):
    """
    Generate documentation for the specified function in the file.
    Args:
        lines (list): A list of lines in the file.
        fn_start_ln (int): The line number where the function starts.
        function_name (str): The name of the function to generate documentation
    """
    # Extract function arguments
    args_match = re.search(r'\(([^)]*)\)', lines[fn_start_ln])
    if args_match:
        # Extract arguments from the updated text
        args_text = args_match.group(1).strip()

        # Ignore if arguments are "void"
        if args_text.lower() == 'void':
            arguments = []
        else:
            while ')' not in args_text and '\n' not in lines[fn_start_ln]:
                # Iterate through the remaining lines until a closing '()'
                #  or a new line is encountered
                fn_start_ln += 1
                args_text += lines[fn_start_ln].strip()

            # Continue searching for closing parenthesis in the line
                # and take the word before it as the second argument
            closing_parenthesis_pos = args_text.find(')')
            if closing_parenthesis_pos != -1:
                args_text = args_text[:closing_parenthesis_pos].strip()

            arguments = args_text.split(',')
            arguments = [arg.strip().split(' ')[-1].
                         lstrip('*') if '*' in arg else arg.strip().
                         split(' ')[-1] for arg in arguments if arg.strip()]

        # Create documentation
        documentation = []
        documentation.append('/**')
        documentation.append(f' * {function_name} - a Function that ...')
        if arguments:
            for arg in arguments:
                # Correctly identify the second argument as
                # the word before the last closing parenthesis
                if arg == arguments[-1]:
                    documentation.append(f' * @{arg}: Description of {arg}.')
                else:
                    documentation.append(f' * @{arg}: Description of {arg}.')
        documentation.append(' * Return: Description of the return value.')
        documentation.append(' */\n')  # Add a new line after closing '/'

        # Insert documentation into the file
        lines.insert(fn_start_ln, '\n'.join(documentation))


def extract_functions_with_no_description(file_path):
    """
    Extract functions with no description from the specified file.
    Args:
        file_path (str): The path of the file to extract functions from.
    Returns:
        list: A list of functions with no description.
    """
    functions = []
    file_path = 'errors.txt'
    with open(file_path, 'r', encoding='utf-8') as errors_file:
        for line in errors_file:
            # Check if the error description contains msg
            if 'no description found for function' in line:
                # Split the line by space and get the word after
                # 'no description found for function'
                words = line.split()
                # Adjust idx based on specific position of the function name
                index = words.index('no') + 5
                function_name = words[index]

                # Append the function name to the list
                functions.append(function_name)

    return functions


def fix_space_between_func_name_open_parenthesis(file_path, ln_num, err_desc):
    """
    Fix space prohibited between function name and
        open parenthesis in the specified file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        ln_num (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Extract specifier from err_desc
    specifier_index = err_desc.find("'") + 1
    specifier = err_desc[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(ln_num) - 1]

    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(f' {specifier}', specifier)

    # Replace the line in the file
    lines[int(ln_num) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_after_that_open_parenthesis(file_path, ln_num, err_desc):
    """
    Fix space prohibited after that open parenthesis in the specified file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        ln_num (str): The line number to fix.
        err_desc (str): The description of the error.

    """
    # Extract specifier from err_desc
    specifier_index = err_desc.find("'") + 1
    specifier = err_desc[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(ln_num) - 1]

    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(f'{specifier} ', specifier)

    # Replace the line in the file
    lines[int(ln_num) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_before_that_close_parenthesis(file_path, ln_num, err_desc):
    """
    Fix space prohibited before that close parenthesis in the specified file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        ln_num (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Extract specifier from err_desc
    specifier_index = err_desc.find("'") + 1
    specifier = err_desc[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(ln_num) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(f' {specifier}', specifier)

    # Replace the line in the file
    lines[int(ln_num) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_required_before_open_parenthesis(file_path, ln_num, err_desc):
    """
    Fix space required before the open parenthesis in the specified file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        ln_num (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Extract specifier from err_desc
    specifier_index = err_desc.find("'") + 1
    specifier = err_desc[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(ln_num) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(specifier, f' {specifier}')

    # Replace the line in the file
    lines[int(ln_num) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_brace_should_be_on_the_next_line(errors_file_path):
    """
    Fix errors in the specified file.
    Args:
        errors_file_path (str): The path of the file to fix errors in.
    """
    errors_fixed = True  # Set to True initially to enter the loop

    while errors_fixed:
        errors_fixed = False  # Reset flag at the beginning of each iteration

        with open(errors_file_path, 'r', encoding='utf-8') as errors_file:
            # Read all lines at once to allow modification list while iterating
            error_lines = errors_file.readlines()

            for i, err_line in enumerate(error_lines):
                if 'that open brace { should be on the next line' in err_line:
                    # Extract (file_path, line_number) from the error line
                    variables = extract_and_print_variables(err_line)
                    if len(variables) >= 2:
                        # Take the first two values
                        f_path, ln_num = variables[:2]

                        # Fix missing blank line after declaration
                        if fix_brace_next_line(f_path, ln_num, 'errors.txt'):
                            errors_fixed = True  # Set flag if a line is fixed

                            # Add a message in the error line
                            error_lines[i] += " (brace moved to the next line)"

                elif ('following function declarations go on '
                      'the next line') in err_line:
                    # Extract (f_path, ln_num) from the error line
                    variables = extract_and_print_variables(err_line)
                    if len(variables) >= 2:
                        # Take the first two values
                        f_path, ln_num = variables[:2]

                        # Fix missing blank line after declaration
                        if fix_brace_next_line(f_path, ln_num, 'errors.txt'):
                            errors_fixed = True  # Set flag if a line is fixed

                            # Add a message in the error line
                            error_lines[i] += " (brace moved to the next line)"


def fix_brace_next_line(file_path, ln_num, errors_file_path):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        ln_num (str): The line number to fix.
        errors_file_path (str): The path of the errors.txt file.
    Returns:
        bool: True if the line is fixed, False otherwise.
    """
    # Convert ln_num to integer
    ln_num = int(ln_num)

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Check if the specified line is within the file's range
    if 1 <= ln_num <= len(lines):
        # Find the brace '{' in the line
        line = lines[ln_num - 1]

        # Replace '{' with '\n{' to move it to the next line
        lines[ln_num - 1] = line.replace('{', '\n{')

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        # Clean 'errors.txt' before extracting new errors
        clean_errors_file(errors_file_path)

        return True  # Line is fixed, return True

    return False


def brace_go_next_line(file_path, line_number, error_description):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        error_description (str): The description of the error.

    """
    specifier = '{'

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Check if the specifier is present in the error description
    if specifier in error_description:
        # Replace the specifier with a newline before the specifier
        fixed_line = error_line.replace(f'{specifier}', f'\n{specifier}')

        # Replace the line in the file
        lines[int(line_number) - 1] = fixed_line

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)


def fix_brace_should_be_on_the_previous_line(errors_file_path):
    """
    Fix errors in the specified file.
    Args:
        errors_file_path (str): The path of the file to fix errors in.
    """
    errors_fixed = True  # Set to True initially to enter the loop

    while errors_fixed:
        errors_fixed = False  # Reset flag at the beginning of each iteration

        with open(errors_file_path, 'r', encoding='utf-8') as errors_file:
            # Read all lines at once allow modification of list while iterating
            error_lines = errors_file.readlines()

            for error_line in error_lines:
                if ('that open brace { '
                        'should be on the previous line') in error_line:
                    # Extract (file_path, line_number) from the error line
                    variables = extract_and_print_variables(error_line)
                    if len(variables) >= 2:
                        # Take the first two values
                        file_path, line_number = variables[:2]

                        # Fix missing blank line after declaration
                        if fix_brace_on_the_previous_line(
                                file_path,
                                line_number,
                                'errors.txt'
                        ):
                            errors_fixed = True  # Set flag if a line is fixed


def fix_brace_on_the_previous_line(file_path, line_number, errors_file_path):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        errors_file_path (str): The path of the errors.txt file.
    Returns:
        bool: True if the line is fixed, False otherwise.
    """
    # Convert line_number to integer
    line_number = int(line_number)

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    line_number -= 1

    # Find the position of the '{' in the previous line
    brace_position = lines[line_number].rfind('{')

    if brace_position == -1:
        return False  # No '{' found in the previous line, no fix needed

    # Remove spaces and newline before the '{'
    lines[line_number] = lines[line_number][:brace_position].rstrip(
    ) + '{' + lines[line_number][brace_position + 1:]

    # Delete the previous '\n' character to move the brace to the previous line
    if lines[line_number - 1].endswith('\n'):
        lines[line_number - 1] = lines[line_number - 1]\
            .rstrip() + ' ' if not lines[line_number - 1]\
            .endswith(' ') else lines[line_number - 1].rstrip()

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    # Clean 'errors.txt' before extracting new errors
    clean_errors_file(errors_file_path)

    return True  # Line is fixed, return True


def fix_space_prohibited_before_semicolon(file_path, line_number, specifier):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        specifier (str): The specifier to fix.
    """

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Replace any space before the semicolon specifier
    fixed_line = error_line.replace(f' {specifier}', specifier)

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_should_be_foo_star_bar(file_path, line_number, error_description):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        error_description (str): The description of the error.
    """
    # Specify the specifier
    specifier = '*'

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Check conditions and fix the line accordingly
    if 'foo** bar' in error_description:
        fixed_line = error_line.replace(f'{specifier} ', f' {specifier}')
    elif 'foo* bar' in error_description:
        fixed_line = error_line.replace(f'{specifier} ', f' {specifier}')
    elif 'foo * bar' in error_description:
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    elif 'foo*bar' in error_description:
        fixed_line = error_line.replace(f'{specifier}', f' {specifier}')
    else:
        # If none of the conditions match, return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_spaces_prohibited_around_that(file_path, line_number, err_desc):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Find the specifier between two single quotes in the err_desc
    specifier_start = err_desc.find("'") + 1
    specifier_end = err_desc.rfind("'")

    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = err_desc[specifier_start:specifier_end]

    # Extract context from the end of err_desc (ctx:context) between : and )
    context_start = err_desc.rfind(':') + 1
    context_end = err_desc.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = err_desc[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Check if the provided line number is within the valid range
    if not 1 <= int(line_number) <= len(lines):
        # Invalid line number, return without making changes
        return

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Fix line according to the context conditions
    if context == 'WxW':
        fixed_line = error_line.replace(f' {specifier} ', f'{specifier}')
    elif context == 'WxV':
        fixed_line = error_line.replace(f' {specifier}', f'{specifier}')
    elif context == 'VxW':
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    else:
        # If the context doesn't match known conditions
        # return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_prohibited_after_that(file_path, line_number, error_description):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        error_description (str): The description of the error.
    """
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")

    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description
    # (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Fix line according to the context conditions
    if context == 'WxW':
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    elif context == 'ExW':
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    else:
        # If the context doesn't match known conditions,
        # return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_prohibited_before_that(file_path, line_number, err_desc):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Find the specifier between two single quotes in the err_desc
    specifier_start = err_desc.find("'") + 1
    specifier_end = err_desc.rfind("'")

    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = err_desc[specifier_start:specifier_end]

    # Extract context from the end of err_desc (ctx:context) between : and )
    context_start = err_desc.rfind(':') + 1
    context_end = err_desc.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = err_desc[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Fix line according to the context conditions
    if context in ['WxV', 'WxO', 'WxE', 'WxW']:
        fixed_line = error_line.replace(f' {specifier}', f'{specifier}')
    else:
        # If the context doesn't match known conditions,
        # return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_spaces_preferred_around_that(file_path, line_number, err_desc):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Find the specifier between two single quotes in the err_desc
    specifier_start = err_desc.find("'") + 1
    specifier_end = err_desc.rfind("'")

    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = err_desc[specifier_start:specifier_end]

    # Extract context from the end of err_desc (ctx:context) between : and )
    context_start = err_desc.rfind(':') + 1
    context_end = err_desc.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = err_desc[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Check if the line already satisfies the condition
    if f' {specifier} ' in error_line:
        # If the required space is already present, skip the fix
        return

    # Fix line according to the context conditions
    if context == 'VxV':
        fixed_line = error_line.replace(f'{specifier}', f' {specifier} ')
    elif context == 'WxV':
        fixed_line = error_line.replace(f' {specifier}', f' {specifier} ')
    elif context == 'VxW':
        fixed_line = error_line.replace(f'{specifier} ', f' {specifier} ')
    else:
        # If the context doesn't match known conditions,
        # return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_required_around_that(file_path, line_number, error_description):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        error_description (str): The description of the error.
    """
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")

    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of
    # error_description (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Check if the line already satisfies the condition
    if f' {specifier} ' in error_line:
        # If the required space is already present, skip the fix
        return

    # Fix line according to the context conditions
    if context == 'VxV':
        fixed_line = error_line.replace(f'{specifier}', f' {specifier} ')
    elif context == 'WxV':
        fixed_line = error_line.replace(f' {specifier}', f' {specifier} ')
    elif context == 'VxW':
        fixed_line = error_line.replace(f'{specifier} ', f' {specifier} ')
    else:
        # If the context doesn't match known conditions,
        # return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_required_after_that(file_path, line_number, error_description):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        error_description (str): The description of the error.
    """
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")

    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description
    # (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Fix line according to the context conditions
    if context in ('WxV', 'VxV'):
        fixed_line = error_line.replace(f'{specifier}', f'{specifier} ')
    else:
        # If the context doesn't match known conditions,
        # return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_required_before_the_open_brace(file_path, line_number, err_desc):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Extract specifier from err_desc
    specifier_index = err_desc.find("'") + 1
    specifier = err_desc[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(specifier, f' {specifier}')

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def fix_space_required_after_the_close_brace(file_path, line_number, err_desc):
    """
    Fix the specified line in the file.
    Args:
        file_path (str): The path of the file to fix the specified line in.
        line_number (str): The line number to fix.
        err_desc (str): The description of the error.
    """
    # Extract specifier from err_desc
    specifier_index = err_desc.find("'") + 1
    specifier = err_desc[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    error_line.replace(
        specifier, f'{specifier} ')  # ❗ Unused variable [Younis]

    # Replace the line in the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


# Example usage
if __name__ == "__main__":
    # Assuming you have an errors.txt file with test data
    ERROR_FILE_PATH = 'errors.txt'
    process_error_file(ERROR_FILE_PATH)
