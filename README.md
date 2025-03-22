# Grit Version Control System

Welcome to `Grit`, my own personal implementation of `Git` using Python. Implements
reading and writing for blob and tree objects and the ability to commit them, similar
to how `Git` implements them. Uses `SHA1` for hashing and `zlib` for compression.

One of the unique parts about this system is its ability to autogenerate commits! I know its hard to summarise all your changes into one line, so just let AI do it.

**Note**: This is a very raw version of `Git`, and should not be used to handle real projects!

## Testing locally

The `grit_program.sh` script is expected to operate on the `.grit` folder inside
the current working directory.

To initialise a repository as a `Grit` repository, follow these steps

```sh
mkdir your-repo && cd your-repo
/path/to/grit-repo/grit_program.sh init
```

### Optimising your setup

To make this easier to type out, you could add a
[shell alias](https://shapeshed.com/unix-alias/):

```sh
alias grit=/path/to/grit-repo/grit_program.sh

mkdir your-repo && cd your-repo
grit init
```

### Available commands

This assumes that you have made a shell alias for the repository.

- `grit init`: Initializes a new Grit repository by creating necessary configuration files like `.gritignore` and a `.grit` directory to store internal data.
- `grit cat-file -p <object_hash>`: Displays the content of an object (such as a blob, tree, or commit) stored in the Grit repository, identified by its unique `<object_hash>`. This is used to view the raw data associated with a specific object.
- `grit hash-object -w <file_name>`: Computes the hash of a file and stores it in the repository. The `-w` flag indicates that the object should be written (or saved) to the `Grit` repository after hashing.
- `grit ls-tree`: Lists the contents of a tree object in the repository. This command can show the files and directories within a commit or branch, typically showing a snapshot of the repository at a particular point in time.
- `grit write-tree`: Creates a tree object from the current state of the working directory, which is a representation of the directory structure and files. This is typically used to record changes to the repository.
- `grit commit-tree`: Creates a commit object from existing tree object and adds user information. The `-m` flag indicates the message, but `--autogenerate` flag indicates you'd like the AI to do it.
