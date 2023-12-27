import os
import shutil
from datetime import datetime

def create_backup(file_path):
    try:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Create a backup copy of the original file with a timestamp in the filename
        backup_filename = f"{os.path.basename(file_path)}_{timestamp}.bak"
        backup_path = os.path.join(os.path.dirname(file_path), backup_filename)

        shutil.copy2(file_path, backup_path)

        print(f"Backup created: {backup_path}")
    except FileNotFoundError:
        print(f"Error creating backup for {file_path}: File not found.")
    except Exception as e:
        print(f"Unexpected error in create_backup for {file_path}: {e}")
