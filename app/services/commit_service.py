import os

from app.services.tree_crud_service import write_tree_object


def commit_tree(ignored_files: list[str]):
    """
    Function to commit tree object.
    """
    current_directory = os.getcwd()
    tree_hash = write_tree_object(current_directory, ignored_files)
    return tree_hash
