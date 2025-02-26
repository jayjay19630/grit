import os


def init():
    """
    Function to initialise directory as grit respository.
    """
    os.mkdir(".grit")
    os.mkdir(".grit/objects")
    os.mkdir(".grit/refs")
    with open(".grit/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    with open(".gritignore", "w") as f:
        f.write(".grit\n")
        f.write(".vscode")
    print("Initialized grit directory.")
