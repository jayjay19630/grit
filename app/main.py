import sys
import os

from app.services.init_service import init
from app.services.blob_crud_service import read_blob_object, write_blob_object
from app.services.tree_crud_service import read_tree_object, write_tree_object


def main():
    current_directory = os.getcwd()
    command = sys.argv[1]

    # Initialise git repository
    if command == "init":
        init()

    # Read blob object and print output of content
    elif command == "cat-file":
        content = read_blob_object()
        print(content, end="")

    # Write blob object to a file based on its hash
    elif command == "hash-object" and sys.argv[2] == "-w":
        file_name = sys.argv[3]
        blob_hash = write_blob_object(file_name)
        print(blob_hash, end="")

    # Read a tree object and print output of content
    elif command == "ls-tree":
        content = read_tree_object()
        for entry in content:
            print(entry)

    # Write tree object recursively
    elif command == "write-tree":
        ignored_files: list[str] = []
        with open(".gritignore", "r") as f:
            for line in f:
                ignored_files.append(line.strip())
        tree_hash = write_tree_object(current_directory, ignored_files)
        print(tree_hash, end="")

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
