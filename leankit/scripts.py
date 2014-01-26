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
            lens.append(len(max([x[i] for x in rows] + [headers[i]], key=lambda x: len(str(x)))))
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
            output.write("%s*S = %s" % (hwidth, row._fields[o], row[i]) + "\n")


def create_parser():
    parser = argparse.ArgumentParser(description="Leankit command-line tool")
    parser.add_argument("command")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    config = Config.load_from_env(os.environ) or Config.load_from_homedir()
    if not config:
        sys.exit("No configuration loaded")

    if args.command == "list-boards":
        board_tuple = namedtuple("Board",["id","title"])
        boards = []
        for board in Boards(config).list():
            boards.append(board_tuple(str(board["board_id"]), board["title"]))
        pprinttable(boards)


if __name__ == "__main__":
    main()
