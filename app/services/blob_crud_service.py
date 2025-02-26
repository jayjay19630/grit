import sys
import zlib
import hashlib
import os


def read_blob_object():
    """
    Function to read single blob object specified from its hash.
    """
    try:
        param_index = sys.argv.index("-p")
    except ValueError:
        raise RuntimeError("Please use the -p marker to denote object hash!")

    object_hash = sys.argv[param_index + 1]
    object_dirname = object_hash[:2]
    object_filename = object_hash[2:]
    object_path = f".grit/objects/{object_dirname}/{object_filename}"

    if not os.path.exists(object_path):
        raise FileNotFoundError(f"Object {object_hash} not found at {object_path}")

    with open(object_path, "rb") as f:
        compressed_bytes = f.read()

    try:
        decompressed_bytes = zlib.decompress(compressed_bytes)
    except zlib.error:
        raise RuntimeError(f"Failed to decompress object {object_hash}")

    try:
        _, content = decompressed_bytes.split(b"\0", 1)
        return content.decode("utf-8")
    except ValueError:
        raise RuntimeError(f"Malformed blob object: {decompressed_bytes}")


def write_blob_object(file_name: str):
    """
    Write a single blob object using a file.
    """
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File {file_name} does not exist")

    with open(file_name, "r") as f:
        content = f.read()

    object_data = f"blob {len(content)}\0{content}".encode("utf-8")
    object_hash = hashlib.sha1(object_data).hexdigest()
    compressed_data = zlib.compress(object_data)

    object_dir = f".grit/objects/{object_hash[:2]}"
    object_path = f"{object_dir}/{object_hash[2:]}"

    os.makedirs(object_dir, exist_ok=True)

    with open(object_path, "wb") as f:
        f.write(compressed_data)

    return object_hash
