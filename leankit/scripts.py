#!/usr/bin/env python
import argparse
import sys
import os
from os.path import abspath, join, dirname
from collections import namedtuple


sys.path.insert(0, abspath(join(dirname(__file__), "..")))


from leankit.config import Config
from leankit.board import Boards


def pprinttable(rows, output=sys.stdout):
    if len(rows) > 1:
        headers = rows[0]._fields
        lens = []
        for i in range(len(rows[0])):
            lens.append(
                len(max([x[i] for x in rows] + [headers[i]],
                    key=lambda x: len(str(x)))))
        formats = []
        hformats = []
        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            hformats.append("%%-%ds" % lens[i])
        pattern = " | ".join(formats)
        hpattern = " | ".join(hformats)
        separator = "-+-".join(["-" * n for n in lens])
        output.write((hpattern + "\n") % tuple(headers))
        output.write(separator + "\n")
        for line in rows:
            output.write((pattern % tuple(line)) + "\n")
    elif len(rows) == 1:
        row = rows[0]
        hwidth = len(max(row._fields, key=lambda x: len(x)))
        for i in range(len(row)):
            output.write("%*s = %s" % (hwidth, row._fields[i], row[i]) + "\n")


def create_parser():
    parser = argparse.ArgumentParser(description="Leankit command-line tool")
    subparsers = parser.add_subparsers(
        title="subcommands", help="subcommand help",
        description="valid subcommands",
        dest="command")
    list_boards = subparsers.add_parser(
        "list-boards",
        help="list all boards in the account")
    list_boards.add_argument(
        "--descriptions",
        help="Output board descriptions",
        default=False, action="store_true")

    show_board = subparsers.add_parser(
        "show-board", help="Display board details")
    show_board.add_argument("board", help="Board id to display")

    show_cards = subparsers.add_parser(
        "show-cards", help="Display lane cards")
    show_cards.add_argument("board", help="Board id to display")
    show_cards.add_argument("lane", help="Lane id to display")

    return parser


def list_boards(config, args):
    board_tuple = namedtuple("Board", ["id", "title"])
    boards = []
    for board in Boards(config).list():
        boards.append(board_tuple(str(board["board_id"]), board["title"]))
    pprinttable(boards)


def show_board(config, args):
    board = Boards(config).get(args.board)
    items = []
    board_tuple = namedtuple("Lane", ["id", "title"])
    for lane in board.lanes:
        items.append(board_tuple(str(lane.id), lane.title))
    pprinttable(items)


def show_cards(config, args):
    board = Boards(config).get(args.board)
    items = []
    card_tuple = namedtuple("Card", ["id", "title", "user", "type"])
    lane = board.get_lane_by_id(int(args.lane))
    for card in lane.cards:
        items.append(
            card_tuple(
                str(card.id),
                card.title,
                card.assigned_user,
                board.card_types[card.type_id]))
    pprinttable(items)


def main():
    parser = create_parser()
    args = parser.parse_args()

    config = Config.load_from_env(os.environ) or Config.load_from_homedir()
    if not config:
        sys.exit("No configuration loaded")

    if args.command == "list-boards":
        list_boards(config, args)

    elif args.command == "show-board":
        show_board(config, args)

    elif args.command == "show-cards":
        show_cards(config, args)

if __name__ == "__main__":
    main()
