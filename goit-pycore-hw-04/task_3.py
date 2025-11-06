import sys
from pathlib import Path
from colorama import init, Fore, Style


def print_tree(path: Path, indent: str = "") -> None:
    """
    Recursively prints the structure of a directory.
    Prints files in green and folders in blue.
    """
    for item in path.iterdir():
        if item.is_file():
            print(f"{indent}{Fore.GREEN}{item.name}{Style.RESET_ALL}")
        elif item.is_dir():
            print(f"{indent}{Fore.BLUE}{item.name}/{Style.RESET_ALL}")
            print_tree(item, indent + "    ")


def main():
    init()

    if len(sys.argv) < 2:
        print("Usage: python task_3.py <path-to-directory>")
        sys.exit(1)

    dir_path = Path(sys.argv[1])

    if not dir_path.exists():
        print(f"Error: path '{dir_path}' does not exist.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{dir_path}' is not a directory.")
        sys.exit(1)

    print(f"{Fore.BLUE}{dir_path.name}/{Style.RESET_ALL}")
    print_tree(dir_path, "    ")


if __name__ == "__main__":
    main()


