import os
import sys
import argparse

def print_file_contents(file_path, file_name):
    if not file_name.endswith(('.txt', '.py', '.md', '.sh', '.json', '.yaml', '.html', '.css', '.js', '.svelte', 'Dockerfile', 'sql')):
        print(f"Message: The file '{file_name}' is not a applicable file.")
        return
    if file_name.endswith(('lock.json', 'package.json', 'package-lock.json', 'congif.js', 'congif.json', 'requirements.txt', 'pyproject.toml', 'pyproject.lock', 'requirements.lock', 'requirements.txt')):
        print(f"Message: The file '{file_name}' is not a applicable file.")
        return
    if not os.path.isfile(file_path):
        print(f"Message: The path '{file_path}' is not a file.")
        return
    if not os.access(file_path, os.R_OK):
        print(f"Message: The file '{file_path}' is not readable.")
        return
    
    try:
        full_path = os.path.join(file_path, file_name)
        with open(full_path, 'r') as file:
            print(f"\nContents of {file_name}:\n")
            print(file.read())
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist in the directory '{file_path}'.")
    except PermissionError:
        print(f"Error: Permission denied for accessing the file '{file_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_directory_contents(directory_path, prefix="", recursive=True):
    '''
    Recursively lists the contents of a directory in a tree-like format.
    Args:
        directory_path (str): The path to the directory to list.
        prefix (str): The prefix for the current level of the tree.
    '''
    if not os.path.isdir(directory_path):
        print(f"Error: The path '{directory_path}' is not a directory.")
        return

    try:
        entries = sorted(os.scandir(directory_path), key=lambda e: e.name)
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            if entry.is_dir() and entry.name in ["__pycache__", "node_modules"]:
                continue
            if entry.name.startswith("."):
                continue

            connector = "└── " if index == entries_count - 1 else "├── "
            print(f"{prefix}{connector}{entry.name}")

            if entry.is_dir() and recursive:
                new_prefix = prefix + ("    " if index == entries_count - 1 else "│   ")
                print_directory_contents(entry.path, new_prefix, recursive)
   
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory_path}'.")

def main():
    parser = argparse.ArgumentParser(description="Print file contents or directory tree.")
    parser.add_argument("-f", "--file", help="Path to the file to print.")
    parser.add_argument("-d", "--directory", help="Path to the directory to list.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively list directory contents.")
    args = parser.parse_args()

    if args.file:
        file_path = os.path.dirname(args.file)
        file_name = os.path.basename(args.file)
        print_file_contents(file_path, file_name)
    elif args.directory:
        print_directory_contents(args.directory, recursive=args.recursive)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()