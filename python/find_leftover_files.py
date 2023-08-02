
import os
import sys

def find_leftover_files(folder):
    # Get the list of all files in the folder and its subdirectories
    files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    # Filter out files starting with "."
    files = [file for file in files if not os.path.basename(file).startswith(".")]
    # Print the list of leftover files
    print("Leftover files:")
    for file in files:
        print(file)

if __name__ == "__main__":
    # Get the command line argument
    if len(sys.argv) != 2:
        print("Usage: python find_leftover_files.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]
    # Run the function
    find_leftover_files(folder)
