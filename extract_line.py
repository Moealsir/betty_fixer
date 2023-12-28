import re


def remove_extra_spaces(input_text):
    lines = input_text.split('\n')
    cleaned_lines = []

    for line in lines:
        cleaned_line = ' '.join(line.split())
        cleaned_lines.append(cleaned_line)

    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text
# Process the errors from the errors.txt file
def process_error_file(errors_file_path):
    with open(errors_file_path, 'r') as errors_file:
        for error_line in errors_file:
            variables = extract_and_print_variables(error_line)
            if variables:
                file_path, line_number, error_description = variables
                fix_errors_from_file(file_path, line_number, error_description)
                
def extract_and_print_variables(error_line):
    # Split the error line to extract variables
    parts = error_line.split(":")
    if len(parts) >= 3:
        # Extracting file path and line number
        file_path, line_number, *error_parts = parts
        # Join all parts except the file path and line number to get the error description
        error_description = ":".join(error_parts[1:]).strip()

        # Further processing if needed
        return file_path.strip(), line_number.strip(), error_description
    return None
def clean_up_line(line):
    # Remove extra spaces and ensure a single space before and after each word
    cleaned_line = ' '.join(part.strip() for part in line.split(' '))

    # Add newline character if the original line had it
    if line.endswith('\n'):
        cleaned_line += '\n'

    return cleaned_line
def fix_errors_from_file(file_path, line_number, error_description):
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
        "Missing a blank line after declarations"
    ]

    # Check each error message
    for i, message in enumerate(error_messages):
        if message in error_description:
            if i == 0:
                fix_space_prohibited_between_function_name_and_open_parenthesis(file_path, line_number, error_description)
            elif i == 1:
                fix_space_prohibited_after_that_open_parenthesis(file_path, line_number, error_description)
            elif i == 2:
                fix_space_prohibited_before_that_close_parenthesis(file_path, line_number, error_description)
            elif i == 3:
                fix_space_required_before_the_open_parenthesis(file_path, line_number, error_description)
            elif i == 4:
                fix_space_prohibited_before_semicolon(file_path, line_number, ';')
            elif i == 5:
                fix_should_be_foo_star_bar(file_path, line_number, error_description)
            elif i == 6:
                fix_spaces_prohibited_around_that(file_path, line_number, error_description)
            elif i == 7:
                fix_space_prohibited_after_that(file_path, line_number, error_description)
            elif i == 8:
                fix_space_prohibited_before_that(file_path, line_number, error_description)
            elif i == 9:
                fix_spaces_preferred_around_that(file_path, line_number, error_description)
            elif i == 10:
                fix_space_required_after_that(file_path, line_number, error_description)
            elif i == 11:
                fix_space_required_around_that(file_path, line_number, error_description)
            elif i == 12:
                fix_space_required_before_the_open_brace(file_path, line_number, error_description)
            elif i == 13:
                fix_space_required_after_the_close_brace(file_path, line_number, error_description)
            # elif i == 14:
            #     fix_missing_blank_line_after_declaration(file_path, line_number)
def fix_missing_blank_line_after_declaration(file_path, line_number):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Insert a newline character at the beginning of the specified line number
    lines.insert(int(line_number) - 1, '\n')

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
# Implement specific fixes for each error type

def remove_unused_attribute(file_name, function_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Search for the function
        pattern = r'\b' + re.escape(function_name) + r'\b[^(]*\([^)]*\)'

        function_declarations = {}  # Dictionary to store function_name and its original line

        for i, line in enumerate(lines):
            if re.search(pattern, line):
                function_start_line = i
                function_declarations[function_name] = lines[function_start_line]  # Save the original line
                break
        else:
                pass
        # took a copy from the original function declaration
        original_declaration = lines[function_start_line]

        # Extract and remove __attribute__((unused))
        match = re.search(r'(__attribute__\s*\(\s*\(\s*unused\s*\)\s*\))', lines[function_start_line])
        unused_attribute = match.group(1) if match else None
        lines[function_start_line] = re.sub(r'__attribute__\s*\(\s*\(\s*unused\s*\)\s*\)', '', lines[function_start_line])

        # Call the existing function to generate documentation
        generate_documentation(lines, function_start_line, file_name, function_name)

        # Restore __attribute__((unused))
        if unused_attribute:
            lines[function_start_line] = lines[function_start_line].replace(lines[function_start_line].strip(), lines[function_start_line].strip() + ' ' + unused_attribute).strip()

        # Write back to the file
        with open(file_name, 'w') as file:
            file.writelines(lines)

        fix_lines_in_file(file_name, function_declarations)
    except Exception as e:
        print(f"Error: {e}")

def fix_lines_in_file(file_name, function_declarations):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Iterate through each line in file
        for i, line in enumerate(lines):
            if '*/' in line and 'unused' in line:
                # Check if any function_name is found in this line
                for func_name, original_line in function_declarations.items():
                    if func_name in line:
                        # Replace the line with the desired format
                        lines[i] = f' */\n{original_line}'
                        
                        # Check if the next line is a blank line; if so, delete it
                        if i + 1 < len(lines) and lines[i + 1] == '\n':
                            del lines[i + 1]
                        break

        # Write back to the file
        with open(file_name, 'w') as file:
            file.writelines(lines)
    except Exception as e:
        print(f"Error: {e}")
                
def generate_documentation(lines, function_start_line, file_name, function_name):
    # Extract function arguments
    args_match = re.search(r'\(([^)]*)\)', lines[function_start_line])
    if args_match:
        # Extract arguments from the updated text
        args_text = args_match.group(1).strip()

        # Ignore if arguments are "void"
        if args_text.lower() == 'void':
            arguments = []
        else:
            while ')' not in args_text and '\n' not in lines[function_start_line]:
                # Iterate through the remaining lines until a closing parenthesis or a new line is encountered
                function_start_line += 1
                args_text += lines[function_start_line].strip()

            # Continue searching for closing parenthesis in the line and take the word before it as the second argument
            closing_parenthesis_pos = args_text.find(')')
            if closing_parenthesis_pos != -1:
                args_text = args_text[:closing_parenthesis_pos].strip()

            arguments = args_text.split(',')
            arguments = [arg.strip().split(' ')[-1].lstrip('*') if '*' in arg else arg.strip().split(' ')[-1] for arg in arguments if arg.strip()]

        # Create documentation
        documentation = []
        documentation.append('/**')
        documentation.append(f' * {function_name} - a Function that ...')
        if arguments:
            for arg in arguments:
                # Correctly identify the second argument as the word before the last closing parenthesis
                if arg == arguments[-1]:
                    documentation.append(f' * @{arg}: Description of {arg}.')
                else:
                    documentation.append(f' * @{arg}: Description of {arg}.')
        documentation.append(' * Return: Description of the return value.')
        documentation.append(' */\n')  # Add a new line after closing '/'

        # Insert documentation into the file
        lines.insert(function_start_line, '\n'.join(documentation))


def extract_functions_with_no_description(file_path):
    functions = []
    file_path = 'errors.txt'
    with open(file_path, 'r') as errors_file:
        for line in errors_file:
            # Check if the error description contains 'no description found for function'
            if 'no description found for function' in line:
                # Split the line by spaces and get the word after 'no description found for function'
                words = line.split()
                index = words.index('no') + 5  # Adjust index based on the specific position of the function name
                function_name = words[index]

                # Append the function name to the list
                functions.append(function_name)

    return functions
def fix_space_prohibited_between_function_name_and_open_parenthesis(file_path, line_number, error_description):
    # Extract specifier from error_description
    specifier_index = error_description.find("'") + 1
    specifier = error_description[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(f' {specifier}', specifier)
    
    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines) 
def fix_space_prohibited_after_that_open_parenthesis(file_path, line_number, error_description):
     # Extract specifier from error_description
    specifier_index = error_description.find("'") + 1
    specifier = error_description[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(f'{specifier} ', specifier)

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_prohibited_before_that_close_parenthesis(file_path, line_number, error_description):
    # Extract specifier from error_description
    specifier_index = error_description.find("'") + 1
    specifier = error_description[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(f' {specifier}', specifier)

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_required_before_the_open_parenthesis(file_path, line_number, error_description):
    # Extract specifier from error_description
    specifier_index = error_description.find("'") + 1
    specifier = error_description[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(specifier, f' {specifier}')

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_prohibited_before_semicolon(file_path, line_number, specifier):

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Replace any space before the semicolon specifier
    fixed_line = error_line.replace(f' {specifier}', specifier)

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_should_be_foo_star_bar(file_path, line_number, error_description): #done
    # Specify the specifier
    specifier = '*'

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Check conditions and fix the line accordingly
    if f'foo* bar' in error_description:
        fixed_line = error_line.replace(f'{specifier} ', f' {specifier}')
    elif f'foo * bar' in error_description:
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    elif f'foo*bar' in error_description:
        fixed_line = error_line.replace(f'{specifier}', f' {specifier}')
    else:
        # If none of the conditions match, return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_spaces_prohibited_around_that(file_path, line_number, error_description):
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")
    
    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the provided line number is within the valid range
    if not (1 <= int(line_number) <= len(lines)):
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
        # If the context doesn't match known conditions, return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def fix_space_prohibited_after_that(file_path, line_number, error_description): #done
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")
    
    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Fix line according to the context conditions
    if context == 'WxW':
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    elif context == 'ExW':
        fixed_line = error_line.replace(f'{specifier} ', f'{specifier}')
    else:
        # If the context doesn't match known conditions, return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_prohibited_before_that(file_path, line_number, error_description):
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")
    
    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Fix line according to the context conditions
    if context == 'WxV' or context == 'WxO' or context == 'WxE' or context == 'WxW':
        fixed_line = error_line.replace(f' {specifier}', f'{specifier}')
    else:
        # If the context doesn't match known conditions, return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_spaces_preferred_around_that(file_path, line_number, error_description): #done
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")
    
    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r') as file:
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
        # If the context doesn't match known conditions, return without making changes
        return  

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_required_around_that(file_path, line_number, error_description): #done
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")
    
    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r') as file:
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
        # If the context doesn't match known conditions, return without making changes
        return  

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_required_after_that(file_path, line_number, error_description):
    # Find the specifier between two single quotes in the error_description
    specifier_start = error_description.find("'") + 1
    specifier_end = error_description.rfind("'")
    
    if specifier_start < 0 or specifier_end < 0:
        # Unable to find valid specifier, return without making changes
        return

    specifier = error_description[specifier_start:specifier_end]

    # Extract context from the end of error_description (ctx:context) between : and )
    context_start = error_description.rfind(':') + 1
    context_end = error_description.rfind(')')

    if context_start < 0 or context_end < 0:
        # Unable to find valid context, return without making changes
        return

    context = error_description[context_start:context_end].strip()

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]

    # Fix line according to the context conditions
    if context == 'WxV':
        fixed_line = error_line.replace(f'{specifier}', f'{specifier} ')
    else:
        # If the context doesn't match known conditions, return without making changes
        return

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_required_before_the_open_brace(file_path, line_number, error_description):
    # Extract specifier from error_description
    specifier_index = error_description.find("'") + 1
    specifier = error_description[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(specifier, f' {specifier}')

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
def fix_space_required_after_the_close_brace(file_path, line_number, error_description):
    # Extract specifier from error_description
    specifier_index = error_description.find("'") + 1
    specifier = error_description[specifier_index:-1]

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the error
    error_line = lines[int(line_number) - 1]
    error_line = clean_up_line(error_line)
    # Find the specifier in the line and fix it
    fixed_line = error_line.replace(specifier, f'{specifier} ')

    # Replace the line in the file
    lines[int(line_number) - 1] = fixed_line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
# Example usage
if __name__ == "__main__":
# Assuming you have an errors.txt file with test data
    errors_file_path = 'errors.txt'
    process_error_file(errors_file_path)
    