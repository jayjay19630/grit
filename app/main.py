import sys
import os
import zlib
import hashlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory.")
    elif command == "cat-file":
        param_index = sys.argv.index("-p")
        if not param_index:
            raise RuntimeError("Please use the -p marker to denote object hash!")

        object_hash = sys.argv[param_index + 1]
        object_dirname = object_hash[:2]
        object_filename = object_hash[2:]
        with open(f".git/objects/{object_dirname}/{object_filename}", "rb") as f:
            compressed_bytes = f.read()
            decompressed_bytes = zlib.decompress(compressed_bytes)
            content = decompressed_bytes.split(b"\0")[1].decode(encoding="utf-8")
        print(content, end="")
    elif command == "hash-object" and sys.argv[2] == "-w":
        file_name = sys.argv[3]
        with open(file_name, "r") as f:
            content = f.read()
            object_hash = hashlib.sha1(f"blob {len(content)}\0 {content}").hexdigest()
        with open(f"{object_hash[:2]}/{object_hash[2:]}", "wb") as f:
            f.write(zlib.compress(content))
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
