def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    unique_lines_file1 = set(lines1) - set(lines2)
    unique_lines_file2 = set(lines2) - set(lines1)

    for line_number, line in enumerate(lines1, start=1):
        if line in unique_lines_file1:
            print(f"Line {line_number} in {file1_path}: {line.strip()}")

    for line_number, line in enumerate(lines2, start=1):
        if line in unique_lines_file2:
            print(f"Line {line_number} in {file2_path}: {line.strip()}")

# Example usage:
file1_path = 'extract_line.py'
file2_path = 'betty_fixer/extract_line.py'
compare_files(file1_path, file2_path)

