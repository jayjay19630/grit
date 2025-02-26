import sys
import zlib
import hashlib
import os


def read_blob_object():
    param_index = sys.argv.index("-p")
    if not param_index:
        raise RuntimeError("Please use the -p marker to denote object hash!")

    object_hash = sys.argv[param_index + 1]
    object_dirname = object_hash[:2]
    object_filename = object_hash[2:]
    with open(f".grit/objects/{object_dirname}/{object_filename}", "rb") as f:
        compressed_bytes = f.read()
        decompressed_bytes = zlib.decompress(compressed_bytes)
        content = decompressed_bytes.split(b"\0")[1].decode(encoding="utf-8")

    return content


def write_blob_object(file_name: str):
    with open(file_name, "r") as f:
        content = f.read()

    object_hash = hashlib.sha1(
        (f"blob {len(content)}\x00{content}").encode(encoding="utf-8")
    ).hexdigest()
    os.makedirs(f".grit/objects/{object_hash[:2]}", exist_ok=True)
    with open(f".grit/objects/{object_hash[:2]}/{object_hash[2:]}", "wb") as f:
        f.write(zlib.compress(content.encode(encoding="utf-8")))

    return object_hash
