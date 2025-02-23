import sys
import os
import zlib


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

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
