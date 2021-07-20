import os
import random


TRASH_BIN = "data/trash_bin"


def make_trash_bin(path):
    os.makedirs(path, exist_ok=True)


def remove_file(path, trash_bin):
    filename = os.path.basename(path)
    destination = f"{trash_bin}/{filename}"

    if os.path.exists(destination):
        suffix = random.random()
        destination = f"{destination}.{suffix}"

    os.rename(path, destination)


def main():
    make_trash_bin(TRASH_BIN)
    remove_file("1.txt", TRASH_BIN)


if __name__ == "__main__":
    main()
