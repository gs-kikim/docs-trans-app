from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
from docs_translate.settings import Settings

from docs_translate import const
from docs_translate.exceptions import ConfigurationError

TEST_PATH = Path.cwd() / 'test_data' / 'md_files_folder'


class TestSettings(TestCase):
    def setUp(self) -> None:
        self.current_path = Path.cwd()
        self.config_file_path = self.current_path / Path('test_data/config.json')
        self.test_path = Path(TEST_PATH)
        self.api_key = 'API_KEY'
        self.service_name = const.TRANSLATION_SERVICE_YANDEX
        self.source_lang = 'en'
        self.target_lang = 'ko'

    @patch('docs_translate.settings.get_cli_args')
    def test_common_launch(self, cli_args_mock):
        cli_args_mock.return_value = '-s {} -S {} -T {}'.format(
            self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)

    @patch('docs_translate.settings.get_cli_args')
    def test_lauch_with_path(self, cli_args_mock):
        cli_args_mock.return_value = '-path {} -s {} -S {} -T {}'.format(
            self.test_path, self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.test_path)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)

    @patch('docs_translate.settings.get_cli_args')
    def test_lauch_with_file(self, cli_args_mock):
        cli_args_mock.return_value = '-c {}'.format(
            self.config_file_path
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.service_name, const.TRANSLATION_SERVICE_GOOGLE)
        self.assertEqual(settings.source_lang, 'ko')
        self.assertEqual(settings.target_lang, 'en')

    @patch('docs_translate.settings.get_cli_args')
    def test_lauch_with_file_and_override(self, cli_args_mock):
        cli_args_mock.return_value = '-c {} -s {} -S {} -T {}'.format(
            self.config_file_path, self.service_name, self.source_lang, self.target_lang
        ).split(' ')
        settings = Settings()
        self.assertEqual(settings.path, self.current_path)
        self.assertEqual(settings.service_name, self.service_name)
        self.assertEqual(settings.source_lang, self.source_lang)
        self.assertEqual(settings.target_lang, self.target_lang)

    @patch('docs_translate.settings.get_cli_args')
    def test_settings_are_not_valid(self, cli_args_mock):
        cli_args_mock.return_value = '-T {}'.format(
            self.target_lang
        ).split(' ')
        settings = Settings()
        with self.assertRaises(ConfigurationError):
            settings.source_lang
