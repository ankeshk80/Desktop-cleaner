import os
import time
import logging

# Configure logging
logging.basicConfig(filename='desktop_cleaner.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define the directory to clean
DIR_TO_CLEAN = os.path.join(os.path.expanduser("~"), "Desktop")

# Set the age threshold for automatic deletion (e.g., 30 days)
AGE_THRESHOLD = 30  # days

# Define which file extensions to target
TARGET_EXTENSIONS = ['.tmp', '.log', '.bak', '.old', '.txt']  # Add more as needed

def get_file_age_in_days(file_path):
    """Return the age of the file in days."""
    file_stat = os.stat(file_path)
    file_creation_time = file_stat.st_mtime
    current_time = time.time()
    age_in_seconds = current_time - file_creation_time
    return age_in_seconds / 86400  # Convert seconds to days

def delete_file(file_path):
    """Delete a file and log the deletion."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            logging.info(f"Deleted file: {file_path}")
            print(f"Deleted file: {file_path}")
        except Exception as e:
            logging.error(f"Failed to delete file: {file_path} - {e}")
            print(f"Error deleting file: {file_path} - {e}")
    else:
        logging.warning(f"File does not exist: {file_path}")
        print(f"File does not exist: {file_path}")

def delete_files_older_than(directory, days=AGE_THRESHOLD, manual=False):
    """Delete files older than the specified number of days."""
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_extension = os.path.splitext(file_name)[1].lower()
            
            # Check if the file matches the target extension
            if file_extension in TARGET_EXTENSIONS:
                file_age_days = get_file_age_in_days(file_path)

                if manual or file_age_days >= days:
                    delete_file(file_path)

def manual_clean():
    """Manually clean the desktop by deleting targeted files."""
    print("Manual cleanup started...")
    delete_files_older_than(DIR_TO_CLEAN, manual=True)

def auto_clean():
    """Automatically clean the desktop based on file age."""
    print(f"Automatic cleanup: Deleting files older than {AGE_THRESHOLD} days...")
    delete_files_older_than(DIR_TO_CLEAN)

if __name__ == "__main__":
    # Run either manual or auto-clean based on user input
    choice = input("Enter '1' for automatic cleanup or '2' for manual cleanup: ")
    if choice == '1':
        auto_clean()
    elif choice == '2':
        manual_clean()
    else:
        print("Invalid option! Please enter 1 or 2.")
