import re

from packaging.version import Version


VERSION_PATTERN_1 = re.compile(r"version = [\"|\'](.+)[\"|\']\n", re.I)
VERSION_PATTERN_2 = re.compile(r"__version__ = [\"|\'](.+)[\"|\']\n")
VERSION_PATTERN_3 = re.compile(r"export const version = [\"|\'](.+)[\"|\'];\n")
VERSION_PATTERN_4 = re.compile(r"\"version\": \"(.+)\",\n")


def search_ver(ver: str) -> str:
    ver_patterns = [
        VERSION_PATTERN_1,
        VERSION_PATTERN_2,
        VERSION_PATTERN_3,
        VERSION_PATTERN_4,
    ]

    for pattern in ver_patterns:
        match = pattern.search(ver)

        if match:
            return match.group(1)


def replace_ver(text, new_ver):
    ver_patterns = dict([
        (VERSION_PATTERN_1, f'version = "{new_ver}"\n'),
        (VERSION_PATTERN_2, f'__version__ = "{new_ver}"\n'),
        (VERSION_PATTERN_3, f'export const version = "{new_ver}";\n'),
        (VERSION_PATTERN_4, f'"version": "{new_ver}",\n'),
    ])

    for pattern, replacement in ver_patterns.items():
        match = pattern.search(text)
        if match:
            return re.sub(pattern, replacement, text, count=1)


def increment_ver(version: str) -> Version:

    if not version:
        raise ValueError("Empty version")

    current = Version(version)

    if current.is_devrelease:
        number = current.dev
        number += 1
        new_ver = f"{current.base_version}.dev{number}"

        return Version(new_ver)

    if current.is_prerelease:
        letter, number = current.pre
        number += 1
        new_ver = f"{current.base_version}.{letter}{number}"

        return Version(new_ver)

    cur = current
    new_ver = f"{cur.major}.{cur.minor}.{cur.micro + 1}"

    return Version(new_ver)
