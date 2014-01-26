from unittest import TestCase
import os

import mock

from leankit.config import Config
from .helpers import get_fixture_path


class ConfigTestCase(TestCase):

    def test_base_url(self):
        """
        Config.base_url should contain the domain and base path for API calls
        for this configuration.
        """
        config = Config("testing", "testing@example.com", "password")
        self.assertEqual(
            "https://testing.leankitkanban.com/Kanban/API/",
            config.base_url)

    def test_get_url_for_path(self):
        """
        Config.get_url_for_path should return the complete URL for a resource
        path based on the base URL.
        """
        config = Config("testing", "testing@example.com", "password")
        self.assertEqual(
            "https://testing.leankitkanban.com/Kanban/API/Boards/12345",
            config.get_url_for_path("Boards/12345"))

    def test_load_from_env(self):
        """
        We can configure the application with appropriate entries in the env.
        """
        env = {"LK_ACCOUNT": "example", "LK_EMAIL": "testing@example.com",
               "LK_PASSWORD": "password", "LK_DATE_FORMAT": "%m/%d/%Y"}
        config = Config.load_from_env(env)
        self.assertEqual("example", config.account)
        self.assertEqual("testing@example.com", config.email)
        self.assertEqual("password", config.password)
        self.assertEqual("%m/%d/%Y", config.date_format)

    def test_load_from_env_with_no_date_format(self):
        """
        If there's no date_format in the environment, we should get a default.
        """
        env = {"LK_ACCOUNT": "example", "LK_EMAIL": "testing@example.com",
               "LK_PASSWORD": "password"}
        config = Config.load_from_env(env)
        self.assertEqual("%m/%d/%Y", config.date_format)

    def test_load_from_missing_env(self):
        """Attempt to load from environment with no config"""
        config = Config.load_from_env({})
        self.assertIsNone(config)

    @mock.patch('leankit.config.expanduser')
    def test_load_from_homedir(self, expanduser_mock):
        """
        Config.load_from_homedir reads a simple config file in
        ~/.luckyrc.
        """
        fixture_path = get_fixture_path("luckyrc")
        expanduser_mock.return_value = fixture_path

        config = Config.load_from_homedir()

        self.assertEqual("newtest", config.account)
        self.assertEqual("newtest@example.com", config.email)
        self.assertEqual("newpassword", config.password)
        self.assertEqual("%Y-%m-%d", config.date_format)

        expanduser_mock.assert_called_once_with("~/.luckyrc")

    @mock.patch('leankit.config.expanduser')
    def test_load_from_missing_homedir_file(self, expanduser_mock):
        """Attempt to load from missing ~/.luckyrc.

        If there's no ~/.luckyrc then Config.load_from_homedir should return
        None.
        """
        fixture_path = get_fixture_path("non-existent-file")
        expanduser_mock.return_value = fixture_path

        config = Config.load_from_homedir()

        self.assertIsNone(config)

    @mock.patch('leankit.config.expanduser')
    def test_load_from_missing_homedir_file(self, expanduser_mock):
        """Attempt to load from missing ~/.luckyrc.

        If there's no ~/.luckyrc then Config.load_from_homedir should return
        None.
        """
        fixture_path = get_fixture_path("non-existent-file")
        expanduser_mock.return_value = fixture_path

        config = Config.load_from_homedir()

        self.assertIsNone(config)

    @mock.patch('leankit.config.expanduser')
    def test_load_from_incomplete_homedir_file(self, expanduser_mock):
        """Attempt to load from incomplete config."""
        fixture_path = get_fixture_path("non-existent-file")
        expanduser_mock.return_value = fixture_path

        incomplete_config = "[config]\naccount = testing\n"
        mock_open = mock.mock_open()
        mock_open.return_value.readline.side_effect = [
            "[config]\naccount = testing\n", ""]

        with mock.patch('__builtin__.open', mock_open):
            config = Config.load_from_homedir()

        self.assertIsNone(config)


