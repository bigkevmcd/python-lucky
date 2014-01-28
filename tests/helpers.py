from os import path
import inspect

from httmock import urlmatch


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


# Creates a closure that matches against the URL we expect
# if mock_requests is provided as a list, then record the
# request objects we receive.
def mock_url(url, fixture, mock_requests=None):
    data = load_fixture(fixture)
    mock_requests = mock_requests

    @urlmatch(path=url)
    def mock_url(url, request):
        if mock_requests is not None:
            mock_requests.append(request)
        return data
    return mock_url

