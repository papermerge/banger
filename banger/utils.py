import re

from packaging.version import Version
from enum import Enum

VERSION_PATTERN_1 = re.compile(r"version = [\"|\'](.+)[\"|\']\n", re.I)
VERSION_PATTERN_2 = re.compile(r"__version__ = [\"|\'](.+)[\"|\']\n")
VERSION_PATTERN_3 = re.compile(r"export const version = [\"|\'](.+)[\"|\'];\n")
VERSION_PATTERN_4 = re.compile(r"\"version\": \"(.+)\",\n")


class IncrementType(Enum):
    MAJOR = 1
    MINOR = 2
    MICRO = 3
    DEV = 4  # make or increment dev part
    PRE = 5  # make or increment a pre-release
    FINAL = 6  # creates a final release from pre-release


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
    inc_type: IncrementType = None
) -> Version:
    """Increments version string"""

    if not version:
        raise ValueError("Empty version")

    current = Version(version)

    if inc_type == IncrementType.MAJOR:  # major increment
        cur = current
        new_ver = f"{cur.major + 1}.0.0"
        return Version(new_ver)
    elif inc_type == IncrementType.MINOR:  # minor increment
        cur = current
        new_ver = f"{cur.major}.{cur.minor + 1}.0"
        return Version(new_ver)
    elif inc_type == IncrementType.MICRO:
        cur = current
        new_ver = f"{cur.major}.{cur.minor}.{cur.micro + 1}"
        return Version(new_ver)
    elif inc_type == IncrementType.DEV:
        cur = current
        if cur.is_devrelease:
            new_ver = f"{cur.base_version}.dev{cur.dev + 1}"
        else:
            new_ver = f"{cur.major}.{cur.minor}.{cur.micro + 1}.dev1"
        return Version(new_ver)
    elif inc_type == IncrementType.PRE:
        cur = current
        if cur.is_prerelease:
            if cur.is_devrelease:
                new_ver = f"{cur.major}.{cur.minor}.{cur.micro}.rc1"
            else:
                letter, num = current.pre
                new_ver = f"{cur.major}.{cur.minor}.{cur.micro}.{letter}{num + 1}"
        else:
            new_ver = f"{cur.major}.{cur.minor}.{cur.micro + 1}.rc1"

        return Version(new_ver)
    elif inc_type == IncrementType.FINAL:
        cur = current
        new_ver = f"{cur.major}.{cur.minor}.{cur.micro}"
        return Version(new_ver)

    # inc_type is not provided
    if current.is_devrelease:
        cur = current
        new_ver = f"{cur.base_version}.dev{cur.dev + 1}"
        return Version(new_ver)
    elif current.is_prerelease:
        cur = current
        letter, number = current.pre
        new_ver = f"{cur.base_version}.{letter}{number + 1}"
        return Version(new_ver)

    cur = current
    new_ver = f"{cur.major}.{cur.minor}.{cur.micro + 1}"

    return Version(new_ver)
