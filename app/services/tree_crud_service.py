import sys
import zlib
import os
import hashlib

from app.services.blob_crud_service import write_blob_object
from app.utils import get_ignore_files


def read_tree_object(object_hash: str) -> list[str]:
    """
    Function for reading a tree object.
    """
    object_dirname = object_hash[:2]
    object_filename = object_hash[2:]

    with open(f".grit/objects/{object_dirname}/{object_filename}", "rb") as f:
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
        return [name for _, name, _ in entries]
    else:
        content = []
        for mode, name, object_hash in entries:
            object_type = "tree" if mode == "040000" else "blob"
            content.append(f"{mode} {object_type} {object_hash} {name}")
        return content


def write_tree_object(directory: str) -> str:
    """
    Create a tree object for given directory.
    Recursively creates tree objects for nested directories.
    """
    entries = []
    ignored_files = get_ignore_files()

    for item in sorted(os.listdir(directory)):
        if item in ignored_files:
            continue

        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            sha1 = write_blob_object(item_path)
            mode = "100644"
        elif os.path.isdir(item_path):
            sha1 = write_tree_object(item_path)
            mode = "040000"
        else:
            continue

        entries.append(f"{mode} {item}\0".encode() + bytes.fromhex(sha1))

    tree_content = b"".join(entries)
    header = f"tree {len(tree_content)}\0".encode()
    store = header + tree_content

    sha1 = hashlib.sha1(store).hexdigest()
    object_dir = os.path.join(".grit", "objects", sha1[:2])
    object_path = os.path.join(object_dir, sha1[2:])

    os.makedirs(object_dir, exist_ok=True)

    with open(object_path, "wb") as f:
        f.write(zlib.compress(store))

    return sha1
