import subprocess
import os
import time


# Function to get the length (number of characters) of the file
def get_file_length(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return len(content)  # Return the number of characters
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return None

# Function to read the last known length from a tracker file
def get_last_length(tracker_file):
    try:
        with open(tracker_file, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return None

# Function to save the current length to the tracker file
def save_length(tracker_file, length):
    with open(tracker_file, 'w') as file:
        file.write(str(length))

# Main function to check for changes in the length of the .txt file
def track_file_length(file_path, tracker_file):
    # Get current length of the file
    current_length = get_file_length(file_path)

    if current_length is None:
        return  # If file doesn't exist, exit the function

    # Get the last saved length from the tracker file
    last_length = get_last_length(tracker_file)

    if last_length is None:
        # If there's no previous record, create one
        save_length(tracker_file, current_length)
        print(f"Tracking started. Initial length: {current_length} characters.")
    else:
        # Check if the length has changed
        if current_length != last_length:
            print(f"File length has changed: {last_length} -> {current_length} characters.")
            # Save the new length to the tracker file
            save_length(tracker_file, current_length)
            commit_and_push()
        else:
            print("No change in file length.")

# Example usage:
file_path = 'tracker.txt'       # Path to the text file you want to track
tracker_file = 'totalChar.txt'  # Path to store the length tracker

# Track changes in file length

def commit_and_push():
    # Navigate to the Git repo directory
    os.chdir("../")

    # Stage the file
    subprocess.run(['git', 'add', "app"])

    # Commit the changes
    commit_message = f"Auto-sync: Updated data on {time.strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(['git', 'commit', '-m', commit_message])

    # Push the changes to GitHub
    subprocess.run(['git', 'push'])



# Main loop to periodically check for changes
def main():
    track_file_length

if __name__ == "__main__":
    main()