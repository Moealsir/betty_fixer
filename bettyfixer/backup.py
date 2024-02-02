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
    except FileNotFoundError:
        print(f"Error creating backup for {file_path}: File not found.")
    except Exception as e:
        print(f"Unexpected error in create_backup for {file_path}: {e}")
