def get_ignore_files():
    ignored_files = []
    with open(".gritignore", "r") as f:
        for line in f:
            ignored_files.append(line)
    return ignored_files
