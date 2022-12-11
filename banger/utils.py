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


def increment_ver(
    version: str,
    major: bool = False,
    minor: bool = False
) -> Version:
    """
    Increments version string.

    :param version: Version string to bump in format <major.minor.micro>
    :param minor: Increment major? Default value = False
    :param minor: Increment minor? Default value = False
    :return: Incremented version string

    By default, increments version's micro part.
    Example:
        2.0.0 -> (default behaviour) 2.0.1
        2.0.1 -> (default behaviour) 2.0.2
        2.0.0b1 -> (default behaviour) 2.0.b3
        2.0.2 -> (when minor=True) 2.1.0
        2.0.2 -> (when major=True) 3.0.0

    When both major=True and minor=True -> ValueError
    """
    if not version:
        raise ValueError("Empty version")

    if major and minor:
        raise ValueError("Major and minor cannot be both True")

    current = Version(version)

    if major:  # major increment
        cur = current
        new_ver = f"{cur.major + 1}.0.0"
        return Version(new_ver)

    if minor:  # minor increment
        cur = current
        if cur.is_prerelease or cur.is_devrelease:
            new_ver = f"{cur.major}.{cur.minor}.0"
        else:
            new_ver = f"{cur.major}.{cur.minor + 1}.0"
        return Version(new_ver)

    # rest of code deals with minor increment

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
