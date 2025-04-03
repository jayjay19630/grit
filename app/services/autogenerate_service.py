import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from app.services.blob_crud_service import read_blob_object
from app.services.tree_crud_service import read_tree_object


def autogenerate_commit(tree_hash: str, parent_hash: str):
    current_tree = read_tree_object(tree_hash)
    parent_tree = read_tree_object(parent_hash)

    changes = detect_changes(parent_tree, current_tree)

    prompt = f"""
    You are an experienced but grumpy software engineer with good principles of commit message naming.
    Commits must start with feat: , refactor: or fix: and must be clearly defined.
    Analyze the following changes and generate a concise commit message:
    Changes:
    ###
    {changes}
    ###
    Commit Message: 
    """

    try:
        response = client.responses.create(model="gpt-3.5-turbo-instruct", input=prompt)
        commit_message = response.output_text
    except Exception as e:
        raise RuntimeError(f"Failed to generate commit message: {e}")

    return commit_message


def detect_changes(parent_tree, current_tree):
    """
    Detect changes between two tree objects and provide detailed context for modified files.

    :param parent_tree: The parent tree object.
    :param current_tree: The current tree object.
    :return: A string describing the changes.
    """
    parent_files = {entry["name"]: entry for entry in parent_tree}
    current_files = {entry["name"]: entry for entry in current_tree}

    changes = []

    # Detect added or modified files
    for file_name, current_entry in current_files.items():
        if file_name not in parent_files:
            changes.append(f"Added: {file_name}")
        elif current_entry["hash"] != parent_files[file_name]["hash"]:
            changes.append(f"Modified: {file_name}")
            # Outline changes in lines for modified files
            try:
                parent_content = read_blob_object(
                    parent_files[file_name]["hash"]
                ).splitlines()
                current_content = read_blob_object(current_entry["hash"]).splitlines()
                line_changes = outline_line_changes(parent_content, current_content)
                changes.append(f"  Changes in {file_name}:\n{line_changes}")
            except Exception as e:
                changes.append(f"  Could not outline changes for {file_name}: {e}")

    # Detect deleted files
    for file_name in parent_files.keys():
        if file_name not in current_files:
            changes.append(f"Deleted: {file_name}")

    return "\n".join(changes)


def outline_line_changes(parent_content, current_content):
    """
    Outline line-by-line changes between two versions of a file.

    :param parent_content: List of lines from the parent version of the file.
    :param current_content: List of lines from the current version of the file.
    :return: A string describing the line-by-line changes.
    """
    from difflib import unified_diff

    diff = unified_diff(
        parent_content,
        current_content,
        lineterm="",
        fromfile="parent",
        tofile="current",
    )
    return "\n".join(diff)
