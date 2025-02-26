import sys

from app.services import init_service
from app.services.blob_crud_service import read_blob_object, write_blob_object
from app.services.tree_crud_service import read_tree_object, write_tree_object


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage

    command = sys.argv[1]

    # Initialise git repository
    if command == "init":
        init_service()

    # Read blob object and print output of content
    elif command == "cat-file":
        read_blob_object()

    # Write blob object to a file based on its hash
    elif command == "hash-object" and sys.argv[2] == "-w":
        write_blob_object()

    # Read a tree object and print output of content
    elif command == "ls-tree":
        read_tree_object()

    # Write tree object recursively
    elif command == "write-tree":
        write_tree_object()

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
