import json
import os
import random


TRASH_BIN = os.path.join("data", "trash_bin")
DB_PATH = os.path.join(TRASH_BIN, "db.json")


def make_trash_bin(path):
    os.makedirs(path, exist_ok=True)


def remove_file(path, trash_bin):
    path = os.path.abspath(path)

    filename = os.path.basename(path)
    destination = os.path.join(trash_bin, filename)
    destination = os.path.abspath(destination)

    if os.path.exists(destination):
        suffix = random.random()
        destination = f"{destination}.{suffix}"

    os.rename(path, destination)

    # update_db
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as db_file:
            json.dump({}, db_file)

    with open(DB_PATH) as f_in:
        data = json.load(f_in)

    data[destination] = path
    with open(DB_PATH, "w") as f_out:
        json.dump(data, f_out, indent=4)


def main():
    make_trash_bin(TRASH_BIN)
    remove_file("1.txt", TRASH_BIN)


if __name__ == "__main__":
    main()
