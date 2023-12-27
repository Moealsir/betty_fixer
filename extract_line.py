import re
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
            # elif i == 11:
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

def fix_spaces_prohibited_around_that(file_path, line_number, error_description): #done
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

# Example usage
if __name__ == "__main__":
# Assuming you have an errors.txt file with test data
    errors_file_path = 'errors.txt'
    process_error_file(errors_file_path)
