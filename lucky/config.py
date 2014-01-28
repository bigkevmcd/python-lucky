from os.path import expanduser
from datetime import datetime
from urlparse import urljoin
from ConfigParser import ConfigParser, NoOptionError

default_date_format = "%m/%d/%Y"


class Config(object):

    def __init__(
            self, account, email, password, date_format=default_date_format):
        self.account = account
        self.email = email
        self.password = password
        self.date_format = date_format

    def parse_date(self, date):
        return datetime.strptime(date, self.date_format)

    @property
    def base_url(self):
        return "https://{account}.leankitkanban.com/Kanban/API/".format(
            account=self.account)

    def get_url_for_path(self, path):
        return urljoin(self.base_url, path)

    @classmethod
    def load_from_env(cls, env):
        """
        Attempts to configure from an os.environ like mapping object.
        
        Returns None if not all the required fields found.
        """
        for key in ["LK_ACCOUNT", "LK_EMAIL", "LK_PASSWORD"]:
            if not key in env:
                return
        return cls(
            env["LK_ACCOUNT"], env["LK_EMAIL"],
            env["LK_PASSWORD"], env.get("LK_DATE_FORMAT", default_date_format))

    @classmethod
    def load_from_homedir(cls):
        """
        Attempts to configure from a ConfigParser file in ~/.luckyrc.

        Returns None if not all the required fields found.
        """
        config_path = expanduser("~/.luckyrc")
        parser = ConfigParser()
        if parser.read([config_path]) == [config_path]:
            if not parser.has_section("config"):
                return None
            if parser.has_option("config", "date_format"):
                date_format = parser.get("config", "date_Format")
            else:
                date_format = default_date_format
            try:
                return cls(
                    parser.get("config", "account"),
                    parser.get("config", "email"),
                    parser.get("config", "password"),
                    date_format
                )
            except NoOptionError:
                return
