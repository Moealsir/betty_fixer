import shutil  # Add the import statement for shutil

def create_backup(file_path):
    try:
        # Create a backup copy of the original file
        backup_path = file_path + '.bak'
        shutil.copy2(file_path, backup_path)
    except FileNotFoundError:
        print(f"Error creating backup for {file_path}: File not found.")
    except Exception as e:
        print(f"Unexpected error in create_backup for {file_path}: {e}")
        
        

        