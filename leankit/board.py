import requests


def dict_from_items(data, items):
    result = []
    for item in items:
        result.append((item.lower(), data[item]))
    return dict(result)


class Boards(object):

    def __init__(self, config):
        self.config = config

    def _get(self, path):
        return requests.get(
            self.config.get_url_for_path(path),
            auth=(self.config.email, self.config.password))

    def list(self):
        """
        Yields dictionaries with details of each of the Boards in the
        configured account.
        """
        response = self._get("Boards")
        for data in response.json()["ReplyData"][0]:
            yield {
                "board_id": data["Id"],
                "title": data["Title"],
                "description": data["Description"],
                "is_archived": data["IsArchived"],
                "created": self.config.parse_date(data["CreationDate"]).date()
            }

    def get(self, board_id):
        response = self._get("Boards/%s" % board_id)
        return Board.create_from_board_json(
            self.config,
            response.json()["ReplyData"][0])


class Board(object):

    def __init__(self, config, board_id, title, description, active):
        self.config = config
        self.id = board_id
        self.title = title
        self.description = description
        self.active = active
        self.lanes = []
        self.card_types = {}

    @classmethod
    def create_from_board_json(cls, config, data):
        board = cls(
            config,
            data["Id"],
            data["Title"],
            data["Description"],
            data["Active"])
        board.lanes = [Lane.create_from_lane_json(config, lane)
                       for lane in data["Lanes"]]
        for card_type in data["CardTypes"]:
            details = dict_from_items(card_type, ["Id", "Name"])
            board
        card_types = {t["Id"]: t["Name"]for t in data["CardTypes"]}
        board.card_types = card_types
        return board

    def get_lane_by_id(self, lane_id):
        """
        Fetch a lane by the numeric id.
        """
        for lane in self.lanes:
            if lane.id == lane_id:
                return lane


class Lane(object):
    def __init__(self, config, lane_id, title, index, card_limit):
        self.id = lane_id
        self.title = title
        self.index = index
        self.card_limit = card_limit

    @classmethod
    def create_from_lane_json(cls, config, data):
        lane = cls(
            config,
            data["Id"],
            data["Title"],
            data["Index"],
            data["CardLimit"]
            )
        lane.cards = [Card.create_from_card_json(config, card)
                     for card in data["Cards"]]
        return lane

class Card(object):
    def __init__(self, config, card_id, title, type_id, assigned_user):
        self.config = config
        self.id = card_id
        self.title = title
        self.type_id = type_id
        self.assigned_user = assigned_user

    @classmethod
    def create_from_card_json(cls, config, data):
        return cls(
            config,
            data["Id"],
            data["Title"],
            data["TypeId"],
            data["AssignedUserName"]
        )