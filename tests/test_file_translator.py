import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

import pytest

from md_translate.file_translator import FileTranslator

prefixture =Path.cwd() /'test_data'

fixture = prefixture /'fixture.md'
fixture_translated = prefixture /'fixture_translated.md'
file_to_test_on = prefixture /'file_to_test_on.md'


@pytest.fixture()
def temp_test_file():
    file_to_test_on.write_text(data=fixture.read_text(), encoding='utf8')
    yield
    file_to_test_on.unlink()


class TestFileTranslator:
    @mock.patch('md_translate.line_processor.get_translator_by_service_name')
    def test_file_translator(self, get_translator_mock, temp_test_file):
        class SettingsMock:
            service_name = 'Google'
            source_lang = 'en'
            target_lang = 'ko'
            api_key = 'TEST_API_KEY'

        translator_mock = Mock()
        translator_mock.return_value = '번역 된 문자열'
        get_translator_mock.return_value = translator_mock
        with FileTranslator(SettingsMock(), file_to_test_on) as file_translator:
            assert isinstance(file_translator, FileTranslator)
            file_translator.leave_original_translate()
        get_translator_mock.assert_called_with(SettingsMock.service_name)
        translator_mock.assert_called_with('Some string for translation\n', from_language='en', to_language='ko')

        assert file_to_test_on.read_text() == fixture_translated.read_text()
