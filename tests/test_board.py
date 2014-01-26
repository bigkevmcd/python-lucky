# Copyright 2014 Kevin McDermott
import json
from datetime import date
from unittest import TestCase

import requests
from httmock import urlmatch, HTTMock

import leankit
from leankit.board import Boards, Board

from .helpers import load_fixture


def mock_url(url, fixture, mock_requests=None):
    data = load_fixture(fixture)
    mock_requests = mock_requests

    @urlmatch(path=url)
    def mock_url(url, request):
        if mock_requests is not None:
            mock_requests.append(request)
        return data
    return mock_url


class BoardsTestCase(TestCase):

    def setUp(self):
        config = leankit.Config("testing", "testing@example.com", "password")
        self.boards = Boards(config)


    def test_list_correct_path_and_authentication(self):
        """Boards.list() returns all boards for the configured account."""
        captured_requests = []
        with HTTMock(mock_url(r"\/Kanban\/API/Boards$", "get_boards.json", captured_requests)):
            boards = list(self.boards.list())
        self.assertEqual(3, len(boards))
        self.assertEqual(1, len(captured_requests))
        self.assertEqual(
            "Basic dGVzdGluZ0BleGFtcGxlLmNvbTpwYXNzd29yZA==",
            captured_requests[0].headers["Authorization"])

    def test_list(self):
        """Boards.list() returns all boards for the configured account."""
        with HTTMock(mock_url(r".*\/Boards$", "get_boards.json")):
            boards = list(self.boards.list())
        self.assertEqual(3, len(boards))

        self.assertEqual({
            "board_id": 101,
            "created": date(2009, 8, 19),
            "description": u"The first test board.",
            "is_archived": False,
            "title": u"Test Board A"}, boards[0])

        self.assertEqual({
            "board_id": 102,
            "created": date(2009, 8, 19),
            "description": u"Extra wide lanes",
            "is_archived": False,
            "title": u"Test Board B"}, boards[1])

        self.assertEqual({
            "board_id": 103,
            "created": date(2009, 8, 19),
            "description": u"",
            "is_archived": False,
            "title": u"Test Board C"}, boards[2])

    def test_list_with_error(self):
        """
        """
        # TODO: Test this with an error response

    def test_get(self):
        """
        Boards.get(board_id) returns the board with the supplied
        identifier.
        """
        with HTTMock(mock_url(r".*\/Boards\/12345$", "get_board.json")):
            board = self.boards.get("12345")

        self.assertEqual("Simple Board", board.title)
        self.assertEqual("Example of a Simple Value Stream", board.description)
        self.assertEqual(False, board.active)
        self.assertEqual(6, len(board.lanes))
        self.assertEqual(
            [u"Ready", u"In Process", u"Development",
             u"Testing", u"Deployment", u"Done"],
            [lane.title for lane in board.lanes])
        self.assertEqual(
            {101303: u'Task',
             101304: u'Feature',
             101305: u'Improvement',
             101306: u'Defect'},
            board.card_types)

    def test_get_with_error(self):
        """
        """
        # TODO: Test this with an error response


#    def test_get_identifiers(self):
#        """
#        Boards.get_identifiers(board_id) returns the identifiers for the board
#        with the specified id.
#        """
#        with HTTMock(mock_url("\Boards/12345/GetBoardIdentifiers", )):
#            result = self.boards.get_identifiers("12345")
#        self.assertEqual({"testing": "testing"}, result)
#
#    def test_get_newer_if_exists(self):
#        """
#        Boards.get_newer_if_exists(board_id, version_id) returns a greater
#        version of the board than the one passed.
#        """
#        with HTTMock(mock_url("\Boards/12345/BoardVersion/123/GetNewerIfExists", )):
#            result = self.boards.get_newer_if_exists("12345", "123")
#        self.assertEqual({"testing": "testing"}, result)
#
#    def test_get_board_history_since(self):
#        """
#        Boards.get_board_history_since(board_id, version_id) returns a greater
#        version of the board than the one passed.
#
#        http://myaccount.leankitkanban.com/Kanban/Api/Board/101000/BoardVersion/213/GetBoardHistorySince
#        """
#        with HTTMock(mock_url("\Boards/12345/BoardVersion/123/GetNewerIfExists", )):
#            result = self.boards.get_newer_if_exists("12345", "123")
#        self.assertEqual({"testing": "testing"}, result)
#
#
class BoardTest(TestCase):

    def setUp(self):
       config = leankit.Config("testing", "testing@example.com", "password")
       self.boards = Boards(config)

    def test_get_lane(self):
        """
        Board.get_lane returns the details for the lane with the specified id.
        """
        with HTTMock(mock_url(r".*\/Boards\/12345$", "get_board.json")):
            board = self.boards.get("12345")
        lane = board.get_lane_by_id(101107)
        self.assertEqual("Ready", lane.title)
        self.assertEqual(2, len(lane.cards))
        self.assertEqual("Sample 11", lane.cards[0].title)
