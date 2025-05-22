import os
import sys

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
        # Get all entries in the directory
        entries = sorted(os.scandir(directory_path), key=lambda e: e.name)
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            # Skip some directories and hidden files
            if entry.is_dir() and entry.name in ["__pycache__", "node_modules"]:
                continue
            # Skip hidden files and directories
            if entry.name.startswith("."):
                continue

            # Determine the connector symbol
            connector = "└── " if index == entries_count - 1 else "├── "
            print(f"{prefix}{connector}{entry.name}")

            # If the entry is a directory, recurse into it
            if entry.is_dir() and recursive:
                # Adjust the prefix for the next level
                new_prefix = prefix + ("    " if index == entries_count - 1 else "│   ")
                print_directory_contents(entry.path, new_prefix)
   
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory_path}'.")


def get_file_contents(file_path):
    '''
    Reads the contents of a file and returns it.
    Args:
        file_path (str): The path to the file to read.
    Returns:
        str: The contents of the file.
    '''
    if not os.path.isfile(file_path):
        print(f"Message: The path '{file_path}' is not a file.")
        return "not a file"
    if not os.access(file_path, os.R_OK):
        print(f"Message: The file '{file_path}' is not readable.")
        return "not readable"    
    # skip pdf, docx, etc.
    if not file_path.endswith(('.txt', '.py', '.md', '.sh', '.json', 'compose.yaml', '.html', '.css', '.js', '.svelte', 'Svelte', 'Dockerfile', 'sql')):
        print(f"Message: The file '{file_path}' is not a applicable file.")
        return "not applicable"
    if file_path.endswith(('lock.json', 'package.json', 'package-lock.json', 'congif.js', 'congif.json', 'pyproject.toml', 'pyproject.lock', 'requirements.lock')):
        print(f"Message: The file '{file_path}' is not a applicable file.")
        return "not applicable"
    
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return "file not found"
    except PermissionError:
        print(f"Error: Permission denied for accessing the file '{file_path}'.")
        return "permission denied"
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"error: {e}"

def get_directory_contents(directory_path, prefix="", recursive=True):
    '''
    Get the contents of a directory. Uses same format as print_directory_contents.
    Args:
        directory_path (str): The path to the directory to list.
        prefix (str): The prefix for the current level of the tree.
        recursive (bool): Whether to list contents recursively.
    Returns:
        str: The contents of the directory.
    '''
    if not os.path.isdir(directory_path):
        print(f"Error: The path '{directory_path}' is not a directory.")
        return
    contents = ""
    try:
        # Get all entries in the directory
        entries = sorted(os.scandir(directory_path), key=lambda e: e.name)
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            # Skip some directories and hidden files
            if entry.is_dir() and entry.name in ["__pycache__", "node_modules"]:
                continue
            if entry.name.startswith("."):
                continue

            # Determine the connector symbol
            connector = "└── " if index == entries_count - 1 else "├── "
            contents += f"{prefix}{connector}{entry.name}\n"

            # If the entry is a directory, recurse into it
            if entry.is_dir() and recursive:
                # Adjust the prefix for the next level
                new_prefix = prefix + ("    " if index == entries_count - 1 else "│   ")
                new_contents = get_directory_contents(entry.path, new_prefix)
                if new_contents:
                    contents += new_contents
        return contents
    
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory_path}'.")

def get_all_file_contents(directory_path):
    '''
    Get the contents of all files in a directory.
    Args:
        directory_path (str): The path to the directory to read.
    Returns:
        dict: A dictionary with file names as keys and their contents as values.
    '''
    if not os.path.isdir(directory_path):
        print(f"Error: The path '{directory_path}' is not a directory.")
        return {}
    
    all_contents = {}
    try:
        for entry in os.scandir(directory_path):
            if entry.is_file():
                new_contents = get_file_contents(entry.path)
                if new_contents not in ["not a file", "not readable", "not applicable", "file not found", "permission denied", "error:"]:
                    all_contents[entry.name] = new_contents
            elif entry.is_dir():
                all_contents.update(get_all_file_contents(entry.path))
        return all_contents
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' does not exist.")
        return {}
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory_path}'.")
        return {}
    
def parse_directory_path(directory_path, prefix="", recursive=True):
    '''
    Parse the directory path and return its contents.
    Args:
        directory_path (str): The path to the directory to parse.
        prefix (str): The prefix for the current level of the tree.
        recursive (bool): Whether to list contents recursively.
        Uses "get_all_file_contents" to get the contents of all files in the directory.
    Returns:
        dict: A dictionary with directory names as keys and their contents as values.
        The key is always appended with the path to the file.
    '''
    if not os.path.isdir(directory_path):
        print(f"Message: The path '{directory_path}' is not a directory.")
        return {}
    
    contents = {}
    try:
        # Get all entries in the directory
        entries = sorted(os.scandir(directory_path), key=lambda e: e.name)
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            # Skip some directories and hidden files
            if entry.is_dir() and entry.name in ["__pycache__", ".git", ".venv", "node_modules", ".vscode", ".idea", ".ollama"]:
                continue
            if entry.name.startswith("."):
                continue

            contents[entry.name] = {}

            # If the entry is a directory, recurse into it
            if entry.is_dir() and recursive:
                # Adjust the prefix for the next level
                new_prefix = prefix + ("    " if index == entries_count - 1 else "│   ")
                contents[entry.name] = parse_directory_path(entry.path, new_prefix)
            elif entry.is_file():
                contents[entry.name] = get_file_contents(entry.path)
            if contents[entry.name] in ["not a file", "not readable", "not applicable", "file not found", "permission denied", "error:"]:
                # delete the entry if it is not a file
                del contents[entry.name]

        return contents

    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return contents

def flatten_dict_with_paths(d, parent_path="", append_root=False):
    """
    Flattens a nested dictionary from parse_directory_path, prepending keys with their full path.
    Args:
        d (dict): The nested dictionary.
        parent_path (str): The path accumulated so far.
    Returns:
        dict: A flat dictionary with full paths as keys.
    """
    flat = {}
    for k, v in d.items():
        current_path = os.path.join(parent_path, k) if parent_path else k
        if isinstance(v, dict):
            flat.update(flatten_dict_with_paths(v, current_path))
        else:
            flat[current_path] = v
    
    if append_root:
        # add ./ to all keys
        flat = {os.path.join("./", k): v for k, v in flat.items()}
    return flat


if __name__ == "__main__":
    
    #print_directory_contents("./documents", "", True)
    #print_file_contents("./documents/mock", "temp.txt")
    res = parse_directory_path("../App/", "", True)
    new_res = flatten_dict_with_paths(res, append_root=True)
    for k, v in new_res.items():
        if isinstance(v, dict):
            print("#############HERE################")
            print(f"{k}:\n{v}")
        else:
            print(f"{k}:\n{v[:50]}...")
            print("--" * 50)