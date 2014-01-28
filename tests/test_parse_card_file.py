import os
import unittest
import tempfile

from lucky.cards import parse_card


class CardFileTestCase(unittest.TestCase):
    __cleanup = []

    def tearDown(self):
        for filename in self.__cleanup:
            if os.path.exists(filename):
                os.unlink(filename)

    def create_file(self, content=None):
        fd, filename = tempfile.mkstemp("", "tmp", None)
        self.__cleanup.append(filename)
        if content is not None:
            os.write(fd, content)
            os.close(fd)
        else:
            os.close(fd)
            os.unlink(filename)
        return filename

    def test_parse_card_with_missing_file(self):
        """
        Running parse_card on a missing file should not trigger an error, but
        should just return a None object.
        """
        filename = self.create_file()
        self.assertIsNone(parse_card(filename))

    def test_parse_card_with_complete_file(self):
        """
        parse_card should split a text file on ---- into a dict with keys
        "title", "body" and "link_url".
        """
        filename = self.create_file(
            "testing\n----\nthis is the body\n----\n"
            "http://bugs.example.com\n")

        result = parse_card(filename)
        self.assertEqual({
            "title": "testing", "body": "this is the body\n",
            "link_url": "http://bugs.example.com"}, result)
