import requests


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
        self.board_id = board_id
        self.title = title
        self.description = description
        self.active = active

    @classmethod
    def create_from_board_json(cls, config, data):
        board = cls(
            config,
            data["Id"],
            data["Title"],
            data["Description"],
            data["Active"])
        board.lanes = data["Lanes"]
        return board
