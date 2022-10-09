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


def test_replace_version_1():
    old_version_text = """
    version = "2.38.0"
    """
    new_version_text = """
    version = "2.38.1"
    """
    assert replace_ver(old_version_text, "2.38.1") == new_version_text


def test_replace_version_2():
    old_version_text = """
    __version__ = "2.38.0"
    """
    new_version_text = """
    __version__ = "2.38.1"
    """
    assert replace_ver(old_version_text, "2.38.1") == new_version_text


def test_increment_ver():
    assert increment_ver("2.1.0b1") == Version("2.1.0b2")
    assert increment_ver("2.1.1") == Version("2.1.2")
    assert increment_ver("2.1.1dev2") == Version("2.1.1dev3")
