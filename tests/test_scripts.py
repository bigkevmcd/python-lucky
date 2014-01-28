# Copyright 2014 Kevin McDermott
from datetime import date
from unittest import TestCase
from cStringIO import StringIO

from httmock import HTTMock

from lucky import scripts
import lucky

from .helpers import mock_url


class ScriptTestCase(TestCase):

    def setUp(self):
        self.config = lucky.Config(
            "testing", "testing@example.com", "password")

    def test_list_boards(self):
        """
        list_boards should output a table with all the boards in the
        account.
        """
        with HTTMock(mock_url(r".*\/Boards$", "get_boards.json")):
            stdout = StringIO()
            scripts.list_boards(self.config, None, output=stdout)
