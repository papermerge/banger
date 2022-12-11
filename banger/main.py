import os

from banger.utils import (
    search_ver,
    increment_ver,
    replace_ver
)


INCREMENTED_PART = ("major", "minor", "micro")


def get_file_content(file_path: str) -> str:

    with open(file_path, "r") as file:
        content = file.read()

    return content


def set_file_content(file_path: str, content: str) -> None:

    with open(file_path, "w") as file:
        file.write(content)


def main():
    files_list = os.environ["INPUT_FILES_LIST"]
    incremented_part = os.environ["INPUT_INCREMENTED_PART"]

    if incremented_part not in INCREMENTED_PART:
        printf(f"incremented_part expected to be one of {INCREMENTED_PART}")
        printf(f"actual value is {incremented_part}")
        return

    # In case multiple files are given only last file's version will be
    # set as output - this means that you need to take care yourself
    # for all versions in given list to be same.
    # Project can have only one version (in the given git branch), right?
    old_version = None
    new_version = None

    for file_path in files_list.split(','):
        file_path = file_path.strip()
        content = get_file_content(file_path)
        old_version = search_ver(content)
        if not old_version:
            print(f"No version detected in file {file_path}")
            continue
        _minor = incremented_part == 'minor'
        _major = incremented_part == 'major'
        new_version = increment_ver(
            old_version,
            minor=_minor,
            major=_major
        )

        print(f"{file_path}: {old_version} -> {new_version}")

        new_content = replace_ver(content, str(new_version))
        set_file_content(file_path, new_content)

    if old_version:
        os.environ['GITHUB_OUTPUT'] = f"old_version={old_version}"
    else:
        print("old version not found")

    if new_version:
        os.environ['GITHUB_OUTPUT'] = f"new_version={new_version}"
    else:
        print("new version not set")



if __name__ == "__main__":
    main()
