import subprocess
import sys

def run_betty(file_path, output_file):
    try:
        # Run Betty on the specified file
        result = subprocess.run(['betty', file_path], capture_output=True, text=True, check=True)

        # Extract the output, including errors and warnings
        output = result.stdout

        # Append the output to the common errors.txt file
        with open(output_file, 'a') as common_output_file:
            common_output_file.write(output)
    except subprocess.CalledProcessError as e:
        # Handle the case when Betty returns a non-zero exit code
        pass
        # Append the error output to the common errors.txt file
        with open(output_file, 'a') as common_output_file:
            common_output_file.write(e.stdout)
            common_output_file.write(e.stderr)

if __name__ == "__main__":
    # Check if at least one file path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python error_extractor.py <file1.c> <file2.c> ...")
        sys.exit(1)

    # Specify the common errors.txt file in the current directory
    common_output_file = 'errors.txt'

    # Clear the content of the errors.txt file before appending new errors
    open(common_output_file, 'w').close()

    # Iterate over each file provided as a command-line argument
    for file_path in sys.argv[1:]:
        run_betty(file_path, common_output_file)
