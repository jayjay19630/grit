import sys
import zlib
import hashlib
import os


def read_tree_object():
    try:
        param_index = sys.argv.index("--name-only")
        object_hash = sys.argv[param_index + 1]
    except ValueError:
        # --name-only flag is missing
        object_hash = sys.argv[sys.argv.index("ls-tree") + 1]
    object_dirname = object_hash[:2]
    object_filename = object_hash[2:]

    with open(f".git/objects/{object_dirname}/{object_filename}", "rb") as f:
        compressed_bytes = f.read()

    decompressed_bytes = zlib.decompress(compressed_bytes)

    # Split the header ("tree <size>\0")
    _, _, body = decompressed_bytes.partition(b"\0")

    entries = []
    while body:
        # Find the mode and name, separated by space and null byte
        mode_end = body.find(b" ")
        name_end = body.find(b"\0", mode_end)

        if mode_end == -1 or name_end == -1:
            break

        mode = body[:mode_end].decode()
        name = body[mode_end + 1 : name_end].decode()

        # The SHA1 hash is exactly 20 bytes
        sha1 = body[name_end + 1 : name_end + 21]

        entries.append((mode, name, sha1.hex()))

        # Move to the next entry
        body = body[name_end + 21 :]

    entries.sort(key=lambda entry: entry[1])

    if "--name-only" in sys.argv:
        for _, name, _ in entries:
            print(name)
    else:
        for mode, name, object_hash in entries:
            object_type = "tree" if mode == "40000" else "blob"
            print(f"{mode} {object_type} {object_hash} {name}")


def write_tree_object():
    pass
