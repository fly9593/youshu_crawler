import os


def list_files(directory, indent=0, ignore_dirs=None):
    """Recursively list files and directories, ignoring specified directories, sorted by name"""
    if ignore_dirs is None:
        ignore_dirs = []

    entries = os.listdir(directory)

    # Separate directories and files
    dirs = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry)) and entry not in ignore_dirs]
    files = [entry for entry in entries if not os.path.isdir(os.path.join(directory, entry))]

    # Sort directories and files
    dirs.sort()
    files.sort()

    # Generate the structure for directories
    result = []
    for entry in dirs:
        path = os.path.join(directory, entry)
        result.append('  ' * indent + '|-- ' + entry + '/')
        result.extend(list_files(path, indent + 1, ignore_dirs))

    # Generate the structure for files
    for entry in files:
        result.append('  ' * indent + '|-- ' + entry)

    return result


def generate_structure_report(directory, ignore_dirs=None):
    """Generate project structure report and save to a file"""
    lines = list_files(directory, ignore_dirs=ignore_dirs)
    report = '\n'.join(lines)
    return report


if __name__ == "__main__":
    project_dir = r'D:\software\code\youshu'  # Replace with your project directory
    ignore_dirs = [".venv",".idea",".git","test","__pycache__",""]  # List of directories to ignore
    structure_report = generate_structure_report(project_dir, ignore_dirs=ignore_dirs)

    # Save report to a file
    with open('PROJECT_STRUCTURE.md', 'w') as f:
        f.write("# Project Structure\n\n")
        f.write('```plaintext\n')
        f.write(structure_report)
        f.write('\n```')

    print("Project structure report generated as PROJECT_STRUCTURE.md")
