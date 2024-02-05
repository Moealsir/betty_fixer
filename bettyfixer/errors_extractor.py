"""
Error Extractor module to extract errors from files using Betty style checker.
"""
import subprocess
import sys


def exctract_errors(file_path, output_file):
    """
    Extract errors from a file using Betty style checker and append them to common errors.txt file.
    Args:
        file_path (str): The path of the file to extract errors from.
        output_file (str): The path of the common errors.txt file to append the errors to.
    """
    try:
        # Run Betty on the specified file
        result = subprocess.run(['betty', file_path],
                                capture_output=True, text=True, check=True)

        # Extract the output, including errors and warnings
        output = result.stdout

        # Append the output to the common errors.txt file
        with open(output_file, 'a', encoding='utf-8') as errors_file_path:
            errors_file_path.write(output)
    except subprocess.CalledProcessError as e:
        # Handle the case when Betty returns a non-zero exit code
        pass # ❗
        # Append the error output to the common errors.txt file
        with open(output_file, 'a', encoding='utf-8') as errors_file_path:
            errors_file_path.write(e.stdout)
            errors_file_path.write(e.stderr)


if __name__ == "__main__":
    # Check if at least one file path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python error_extractor.py <file1.c> <file2.c> ...")
        sys.exit(1)

    # Specify the common errors.txt file in the current directory
    ERROR_FILE_PATH = 'errors.txt'

    # Clear the content of the errors.txt file before appending new errors
    open(ERROR_FILE_PATH, 'w', encoding='utf-8').close()

    # Iterate over each file provided as a command-line argument
    for FILE_PATH in sys.argv[1:]:
        exctract_errors(FILE_PATH, ERROR_FILE_PATH)
