import sys
import os
import zlib
import hashlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage

    command = sys.argv[1]

    # Initialise git repository
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory.")

    # Read blob object and print output of content
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

    # Write blob object to a file based on its hash
    elif command == "hash-object" and sys.argv[2] == "-w":
        file_name = sys.argv[3]

        with open(file_name, "r") as f:
            content = f.read()

        object_hash = hashlib.sha1(
            (f"blob {len(content)}\x00{content}").encode(encoding="utf-8")
        ).hexdigest()
        os.makedirs(f".git/objects/{object_hash[:2]}", exist_ok=True)
        with open(f".git/objects/{object_hash[:2]}/{object_hash[2:]}", "wb") as f:
            f.write(zlib.compress(content.encode(encoding="utf-8")))
        print(object_hash)

    # Read a tree object and print output of content
    elif command == "ls-tree":
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

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
