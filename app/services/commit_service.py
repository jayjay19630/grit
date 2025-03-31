import os
import hashlib
import zlib
import sys


def read_commit_tree():
    """
    Function to read commit object.
    """

    object_hash = sys.argv[2]
    object_dirname = object_hash[:2]
    object_filename = object_hash[2:]
    object_path = f"./grit/objects/{object_dirname}/{object_filename}"

    with open(object_path, "rb") as f:
        compressed_bytes = f.read()

    try:
        decompressed_bytes = zlib.decompress(compressed_bytes)
    except zlib.error:
        raise RuntimeError(f"Failed to decompress commit object {object_hash}")

    try:
        _, content = decompressed_bytes.split(b"\0", 1)
        return content.decode("utf-8")
    except ValueError:
        raise RuntimeError(f"Malformed commit object: {decompressed_bytes}")


def commit_tree(
    tree_hash: str, commit_message: str, parent_hash: str | None = None
) -> str:
    """
    Function to commit tree object that has already been written.
    """

    # TODO: Change these variables so that they match the user directly.
    author_name = "John Doe"
    author_email = ""
    author_date = ""

    object_content = f"tree {tree_hash}\n"
    if parent_hash:
        object_content = "parent {parent_hash}\n" + object_content
    object_content += f"author {author_name} <{author_email}> {author_date}\n"
    object_content += f"committer {author_name} <{author_email}> {author_date}\n\n"
    object_content += commit_message

    object_data = f"commit {len(object_content)}\0{object_content}".encode("utf-8")
    object_hash = hashlib.sha1(object_data).hexdigest()
    compressed_data = zlib.compress(object_data)

    object_dir = f".grit/objects/{object_hash[:2]}"
    object_path = f"{object_dir}/{object_hash[2:]}"

    os.makedirs(object_dir, exist_ok=True)

    with open(object_path, "wb") as f:
        f.write(compressed_data)

    return object_hash
