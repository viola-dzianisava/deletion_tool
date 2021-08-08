import json
import os
import random
import argparse


TRASH_BIN = os.path.abspath(os.path.join("data", "trash_bin"))
DB_PATH = os.path.join(TRASH_BIN, "db.json")


def make_trash_bin(path):
    os.makedirs(path, exist_ok=True)


def remove_file(path, trash_bin):
    path = os.path.abspath(path)

    if path.startswith(trash_bin):
        raise Exception("File is already in the trash bin")

    filename = os.path.basename(path)
    destination = os.path.join(trash_bin, filename)
    destination = os.path.abspath(destination)

    if os.path.exists(destination):
        suffix = random.random()
        destination = f"{destination}.{suffix}"

    os.rename(path, destination)
    data = open_db()
    data[destination] = path
    write_to_db(data)


def open_db():
    data = {}
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as f_in:
            data = json.load(f_in)
    return data


def write_to_db(data):
    with open(DB_PATH, "w") as f_out:
        json.dump(data, f_out, indent=4)


def restore_file(filename, trash_bin):
    key = os.path.join(trash_bin, filename)
    data = open_db()
    old_path = data.pop(key)
    os.rename(key, old_path)
    write_to_db(data)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', type=str, nargs='+',
        help='files for deletion')
    parser.add_argument('--restore', action='store_true')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    make_trash_bin(TRASH_BIN)
    if args.restore:
        for filename in args.filenames:
            restore_file(filename, TRASH_BIN)
    else:
        for filename in args.filenames:
            remove_file(filename, TRASH_BIN)


if __name__ == "__main__":
    main()
