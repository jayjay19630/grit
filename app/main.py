import sys
import os

from app.services import autogenerate_service
from app.services.commit_service import commit_tree, read_commit
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
        try:
            param_index = sys.argv.index("-p")
        except ValueError:
            raise RuntimeError("Please use -p marker to denote object hash!")

        try:
            object_hash = sys.argv[param_index + 1]
        except IndexError:
            raise RuntimeError("Blob object hash could not be found.")

        content = read_blob_object(object_hash)
        print(content, end="")

    # Write blob object to a file based on its hash
    elif command == "hash-object":
        try:
            param_index = sys.argv.index("-w")
        except ValueError:
            raise RuntimeError("Please use -w marker to denote blob should be written!")

        try:
            file_name = sys.argv[param_index + 1]
        except IndexError:
            raise RuntimeError("Blob object hash could not be found.")

        blob_hash = write_blob_object(file_name)
        print(blob_hash, end="")

    # Read a tree object and print output of content
    elif command == "ls-tree":
        try:
            if "--name-only" in sys.argv:
                param_index = sys.argv.index("--name-only")
                object_hash = sys.argv[param_index + 1]
            else:
                object_hash = sys.argv[sys.argv.index("ls-tree") + 1]
        except IndexError:
            raise RuntimeError("Tree object hash could not be found.")

        content = read_tree_object(object_hash)
        for entry in content:
            print(entry)

    # Write tree object recursively
    elif command == "write-tree":
        tree_hash = write_tree_object(current_directory)
        print(tree_hash, end="")

    elif command == "commit-tree":
        # Get tree hash
        tree_index = sys.argv[2] + 1
        tree_hash = sys.argv[tree_index]

        # Get parent commit hash
        parent_hash = None
        if "-p" in sys.argv:
            try:
                parent_index = sys.argv.index("-p") + 1
                parent_hash = sys.argv[parent_index]
            except:
                raise RuntimeError("Parent commit object hash could not be found.")

        # Get commit message
        if "--autogenerate" in sys.argv and parent_hash is not None:
            commit_message = autogenerate_service(tree_hash, parent_hash)
        else:
            try:
                message_index = sys.argv.index("-m") + 1
                commit_message = sys.argv[message_index]
            except IndexError:
                raise RuntimeError("Commit object message could not be found")

        commit_hash = commit_tree(tree_hash, commit_message, parent_hash)
        print(commit_hash, end="")

    elif command == "cat-commit":
        try:
            object_hash = sys.argv[2]
        except IndexError:
            raise RuntimeError("Commit object hash could not be found")

        content = read_commit(object_hash)
        print(content, end="")

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
