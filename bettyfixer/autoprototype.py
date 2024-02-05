"""
This module contains the functions to generate a header file with
the prototypes of the functions in a directory.
"""
import subprocess
import os
import glob
from colorama import Fore


def betty_check():
    """Check if betty is installed and if there are any errors in the files.
    Returns:
        bool: True if betty is installed and there are no errors, False otherwise.
    """
    try:
        c_files = glob.glob("*.c")
        result1 = subprocess.run(["betty"] + c_files, check=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    except subprocess.CalledProcessError as e:
        print(e)
        return False

    if "ERROR:" in result1.stdout or "ERROR:" in result1.stderr:
        return False
    if "WARNING:" in result1.stdout or "WARNING:" in result1.stderr:
        return False

    return result1.returncode == 0


def print_check_betty_first():
    """Prints a message to the user to fix betty errors first."""
    print(
        Fore.RED + "You should fix betty Errors first before \
            copy prototype functions into The header file" + Fore.RESET
    )


def print_header_name_missing():
    """Prints a message to the user to provide a header file name."""
    print(Fore.RED + "Usage : bettyfixer -H <heahdername>.h" + Fore.RESET)


def print_ctags_header_error(msg):
    """Prints a message to the user in red color."""
    print(Fore.RED + msg + Fore.RESET)


def check_ctags():
    """Check if ctags is installed.
    Returns:
        bool: True if ctags is installed, False otherwise.
        str: Error message if ctags is not installed.
    """
    try:
        subprocess.run(['ctags', '--version'], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)
        return True, None
    except subprocess.CalledProcessError:
        msg = "ctags is not installed. Please install ctags before running this script."
        return False, msg


def generate_tags(directory):
    """Generate tags for the files in the directory.
    Args:
        directory (str): Directory path.
    Returns:
        bool: True if ctags is generated successfully, False otherwise.
    """
    try:
        subprocess.run(['ctags', '-R', '--c-kinds=+p', '--fields=+S', '--extra=+q',
                       '--languages=c', '--langmap=c:.c', directory], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print_ctags_header_error(f"Error generating ctags: {e}")
        return False


def filter_tags(directory, tags_file):
    """
    Filter the tags file to get only the function prototypes.
    Args:
        directory (str): Directory path.
        tags_file (str): Tags file name.
    Returns:
        str: Filtered tags.
    """
    temp_tags_path = os.path.join(directory, 'temp_tags')
    tags_path = os.path.join(directory, tags_file)

    sed_command = (
        f"cat {tags_path} | sed -n 's/^.*\\/\\(.*\\)/\\1/p'  | "
        f"sed 's/\\(.*\\)\\$.*/\\1/' | sed 's/;$//' | uniq | "
        f"sed '/int main(/d' | sed '/.*:/d' | sed 's/$/;/g' > {temp_tags_path}"
    )

    # Run the sed_command using subprocess
    subprocess.run(sed_command, shell=True, check=True)

    # Check if the file exists before trying to open it
    if os.path.exists(temp_tags_path):
        with open(temp_tags_path, 'r', encoding='utf-8') as temp_tags_file:
            filtered_tags = temp_tags_file.read()
        return filtered_tags

    # Handle the case where the file doesn't exist
    msg = f"Error: File {temp_tags_path} does not exist."
    print_ctags_header_error(msg)
    return None


def create_header(header_file, filtered_tags):
    """
    Create a header file with the filtered tags.
    Args:
        header_file (str): Header file name.
        filtered_tags (str): Filtered tags.
    """
    header_name = header_file.split('/')[-1]
    header_name = header_name.split('.')
    header_name = '_'.join(header_name)
    with open(header_file, 'w', encoding='utf-8') as header:
        header.write(f'#ifndef {header_name.upper()}\n')
        header.write(f'#define {header_name.upper()}\n\n')
        header.write(filtered_tags)
        header.write('\n#endif\n')


def delete_files(tags, temp_tags):
    """
    Delete the tags and temp_tags files.
    Args:
        tags (str): Tags file name.
        temp_tags (str): Temp tags file name.
    """
    command = f"rm {tags} {temp_tags}"
    subprocess.run(command, shell=True, check=True)


def check_header_file(header_file):
    """
    Check if the header file is valid.
    Args:
        header_file (str): Header file name.
    Returns:
        bool: True if the header file is valid, False otherwise.
        str: Error message if the header file is invalid.
    """
    if not header_file.endswith('.h'):

        msg = "Error: Invalid header file. It should have a '.h' extension."
        return False, msg
    return True, None


def autoproto(directory, header):
    """
    Generate a header file with the prototypes of the functions in the directory.
    Args:
        directory (str): Directory path.
        header (str): Header file name.
    """
    check1, msg1 = check_header_file(header)
    check2, msg2 = check_ctags()
    if not check1:
        print_ctags_header_error(msg1)
    elif not check2:
        print_ctags_header_error(msg2)
    if generate_tags(directory) is not False:
        filtered_tags = filter_tags(directory, 'tags')
        if filtered_tags is not None:
            create_header(header, filtered_tags)
            delete_files('tags', 'temp_tags')
