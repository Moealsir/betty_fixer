"""
This module provides a function to create a backup copy of a file.
"""
import shutil


def create_backup(file_path):
    """
    Create a backup copy of the original file.
    Args:
        file_path (str): The path of the file to create a backup of.
    """
    try:
        backup_path = file_path + '.bak'
        shutil.copy2(file_path, backup_path)
    except shutil.SameFileError:
        print(
            f"Err creating backup {file_path}: Src and dest are same file.")
    except FileNotFoundError:
        print(f"Error creating backup for {file_path}: File not found.")
    except IsADirectoryError:
        print(f"Error creating backup for {file_path}: Is a directory error.")
    except PermissionError:
        print(f"Error creating backup for {file_path}: Permission error.")
    except OSError as e:
        print(f"Unexpected error in create_backup for {file_path}: {e}")
