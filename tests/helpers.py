from os import path
import inspect


def get_fixture_path(fixture_name):
    """
    Returns the path to a fixture relative to the file the caller is in.
    """
    caller_path = inspect.getfile(inspect.currentframe().f_back)
    return path.join(path.dirname(caller_path), "fixtures", fixture_name)


def load_fixture(fixture_name):
    """
    Opens the named fixture from the fixtures directory of the current file and
    returns the content.
    """
    return open(get_fixture_path(fixture_name), "r").read()
