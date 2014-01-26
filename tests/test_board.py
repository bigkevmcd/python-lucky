# Copyright 2014 Kevin McDermott
import json
from datetime import date
from unittest import TestCase
import pprint

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


test_lanes = {
    101101: "Backlog",
    101102: "Archive",
    101103: "Analysis",
    101104: "Development",
    101105: "Testing",
    101106: "Done",
    101107: "Analysis:Ready",
    101108: "Analysis:In Process",
    101109: "Development:Ready",
    101110: "Development:In Process",
    101111: "Testing:Ready",
    101112: "Testing:In Process",
    101113: "Deployment",
    101114: "Deployment:Ready",
    101115: "Deployment:In Process"
}


class BoardsTestCase(TestCase):

    def setUp(self):
        config = leankit.Config("testing", "testing@example.com", "password")
        self.boards = Boards(config)

    def test_list_correct_path_and_authentication(self):
        """Boards.list() returns all boards for the configured account."""
        captured = []
        mock_request = mock_url(
            r"\/Kanban\/API/Boards$", "get_boards.json", captured)
        with HTTMock(mock_request):
            boards = list(self.boards.list())
        self.assertEqual(3, len(boards))
        self.assertEqual(1, len(captured))
        self.assertEqual(
            "Basic dGVzdGluZ0BleGFtcGxlLmNvbTpwYXNzd29yZA==",
            captured[0].headers["Authorization"])

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
            ["Ready", "In Process", "Development",
             "Testing", "Deployment", "Done"],
            [lane.title for lane in board.lanes])
        self.assertEqual(
            {101303: "Task",
             101304: "Feature",
             101305: "Improvement",
             101306: "Defect"},
            board.card_types)

    def test_get_with_error(self):
        """
        """
        # TODO: Test this with an error response

    def test_get_identifiers(self):
        """
        Boards.get_identifiers(board_id) returns the identifiers for the board
        with the specified id.
        """
        mock_request = mock_url(
            r".*\/Boards\/12345/GetBoardIdentifiers$",
            "get_board_identifiers.json")
        with HTTMock(mock_request):
            result = self.boards.get_identifiers(12345)
        self.assertEqual(
            {101303: u"Task",
             101304: u"Feature",
             101305: u"Improvement",
             101306: u"Defect"}, result["card_types"])
        self.assertEqual({1: "demouser@leankitkanban.com"}, result["users"])
        self.assertEqual(test_lanes, result["lanes"])
        self.assertEqual({
            101404: "Standard",
            101405: "Expedite",
            101406: "Regulatory",
            101407: "Date Dependent"}, result["classes_of_service"])
        self.assertEqual({
            0: "Low",
            1: "Normal",
            2: "High",
            3: "Critical"}, result["priorities"])

    def test_get_identifiers_with_error(self):
        """
        """
        # TODO: Test this with an error response

#    def test_get_newer_if_exists(self):
#        """
#        Boards.get_newer_if_exists(board_id, version_id) returns a greater
#        version of the board than the one passed.
#        """

#    def test_get_board_history_since(self):
#        """
#        Boards.get_board_history_since(board_id, version_id) returns a greater
#        version of the board than the one passed.
#
#        http://myaccount.leankitkanban.com/Kanban/Api/Board/101000/BoardVersion/213/GetBoardHistorySince
#        """


class BoardTest(TestCase):

    def setUp(self):
        config = leankit.Config("testing", "testing@example.com", "password")
        self.boards = Boards(config)

    def test_get_lane_by_id(self):
        """
        Board.get_lane_by_id returns the details for the lane with the
        specified id.
        """
        with HTTMock(mock_url(r".*\/Boards\/12345$", "get_board.json")):
            board = self.boards.get("12345")
        lane = board.get_lane_by_id(101107)
        self.assertEqual("Ready", lane.title)
        self.assertEqual(2, len(lane.cards))
        self.assertEqual("Sample 11", lane.cards[0].title)

    def test_get_lane_by_title(self):
        """
        Board.get_lane_by_title returns the details for the lane with the
        specified title.
        """
        with HTTMock(mock_url(r".*\/Boards\/12345$", "get_board.json")):
            board = self.boards.get("12345")
        lane = board.get_lane_by_title("Ready")
        self.assertEqual(101107, lane.id)
        self.assertEqual("Ready", lane.title)
        self.assertEqual(2, len(lane.cards))
        self.assertEqual("Sample 11", lane.cards[0].title)
