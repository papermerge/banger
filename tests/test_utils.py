import pytest

from packaging.version import Version

from banger.utils import search_ver, increment_ver, replace_ver


def test_search_version_1():
    text = """
    version = "2.38.0"
    """
    assert search_ver(text) == "2.38.0"


def test_search_version_2():
    text = """
    version = '2.1.0b2'
    """
    assert search_ver(text) == "2.1.0b2"


def test_search_version_3():
    text = """
    __version__ = '2.1.0b2'
    """
    assert search_ver(text) == "2.1.0b2"


def test_search_version_4():
    text = """
    VERSION = '1.0.6'
    """
    assert search_ver(text) == "1.0.6"


def test_search_version_5():
    text = """
    VERSION = "1.0.6"
    """
    assert search_ver(text) == "1.0.6"


def test_search_version_js_1():
    text = """
    export const version = '2.1.0b8';
    """
    assert search_ver(text) == "2.1.0b8"


def test_search_version_js_2():
    text = """
    export const version = "2.1.0b8";
    """
    assert search_ver(text) == "2.1.0b8"


def test_search_version_json_1():
    text = """{
        "name": "papermerge",
        "version": "2.1.0b8",
        "private": false,
        "description": "Papermerge DMS frontend"
    }
    """
    assert search_ver(text) == "2.1.0b8"


def test_replace_version_1():
    old_version_text = """
    version = "2.38.0"
    """
    new_version_text = """
    version = "2.38.1"
    """
    assert replace_ver(old_version_text, "2.38.1") == new_version_text


def test_replace_version_with_twist():
    """
    Notice that package dependency 'shinx-multiversion may cause
    unexpected side effect (i.e. may be unwillingly incremented) bacause
    of xxxxversion = "..."
    """
    old_version_text = """
        [tool.poetry]
        name = "documentation"
        version = "1.4.12"
        description = "Papermerge Documentation"
        authors = ["Eugen Ciur <eugen@papermerge.com>"]
        license = "Apache 2.0"

        [tool.poetry.dependencies]
        python = "^3.10"
        Sphinx = "^4.3.2"
        sphinx-rtd-theme = "^1.0.0"
        sphinx-autobuild = "^2021.3.14"
        sphinx-multiversion = "^0.2.4"
        sphinxcontrib-httpdomain = "^1.8.0"
    """
    new_version_text = """
        [tool.poetry]
        name = "documentation"
        version = "1.4.13"
        description = "Papermerge Documentation"
        authors = ["Eugen Ciur <eugen@papermerge.com>"]
        license = "Apache 2.0"

        [tool.poetry.dependencies]
        python = "^3.10"
        Sphinx = "^4.3.2"
        sphinx-rtd-theme = "^1.0.0"
        sphinx-autobuild = "^2021.3.14"
        sphinx-multiversion = "^0.2.4"
        sphinxcontrib-httpdomain = "^1.8.0"
    """
    assert replace_ver(old_version_text, "1.4.13") == new_version_text

def test_replace_version_2():
    old_version_text = """
    __version__ = "2.38.0"
    """
    new_version_text = """
    __version__ = "2.38.1"
    """
    assert replace_ver(old_version_text, "2.38.1") == new_version_text


def test_replace_version_js():
    old_version_text = """
    export const version = "2.1.0b8";
    """
    new_version_text = """
    export const version = "2.1.0b9";
    """
    assert replace_ver(old_version_text, "2.1.0b9") == new_version_text


def test_replace_version_json():
    old_version_text = """{
        "name": "papermerge",
        "version": "2.1.0b8",
        "private": false,
        "description": "Papermerge DMS frontend"
    }
    """
    new_version_text = """{
        "name": "papermerge",
        "version": "2.1.0b9",
        "private": false,
        "description": "Papermerge DMS frontend"
    }
    """
    assert replace_ver(old_version_text, "2.1.0b9") == new_version_text


def test_increment_ver():
    assert increment_ver("2.1.0b1") == Version("2.1.0b2")
    assert increment_ver("2.1.1") == Version("2.1.2")
    assert increment_ver("2.1.1dev2") == Version("2.1.1dev3")


def test_increment_ver_minor():
    assert increment_ver("2.1.0b22", minor=True) == Version("2.1.0")
    assert increment_ver("2.1.0", minor=True) == Version("2.2.0")


def test_increment_ver_major():
    assert increment_ver("2.1.0b22", major=True) == Version("3.0.0")
    assert increment_ver("2.1.0", major=True) == Version("3.0.0")


def test_try_to_increment_both_minor_and_major():
    with pytest.raises(ValueError):
        increment_ver("2.1.0", minor=True, major=True)
