import sys
import os

from app.services import autogenerate_service
from app.services.commit_service import commit_tree, read_commit_tree
from app.services.init_service import init
from app.services.blob_crud_service import read_blob_object, write_blob_object
from app.services.tree_crud_service import read_tree_object, write_tree_object


def get_ignore_files():
    ignored_files: list[str] = []
    with open(".gritignore", "r") as f:
        for line in f:
            ignored_files.append(line)
    return ignored_files


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
        ignored_files = get_ignore_files()
        tree_hash = write_tree_object(current_directory, ignored_files)
        print(tree_hash, end="")

    elif command == "commit-tree":
        # Get tree hash
        tree_index = sys.argv[2] + 1
        tree_hash = sys.argv[tree_index]

        # Get parent commit hash
        parent_hash = None
        if "-p" in sys.argv:
            parent_index = sys.argv.index("-p") + 1
            parent_hash = sys.argv[parent_index]

        # Get commit message
        if "--autogenerate" in sys.argv and parent_hash is not None:
            commit_message = autogenerate_service(tree_hash, parent_hash)
        else:
            message_index = sys.argv.index("-m") + 1
            commit_message = sys.argv[message_index]

        commit_hash = commit_tree(tree_hash, commit_message, parent_hash)
        print(commit_hash, end="")

    elif command == "cat-commit":
        content = read_commit_tree()
        print(content, end="")

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
