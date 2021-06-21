from pathlib import Path

import pytest

from docs_translate.exceptions import ObjectNotFoundException, DocsFileNotFoundError
from docs_translate.files_worker import FilesWorker

TEST_FIRST_FILE = Path.cwd() / 'tests/test_data/md_files_folder/first_file.md'
TEST_SECOND_FILE = Path.cwd() / 'tests/test_data/md_files_folder/second_file.md'


class SettingsMock:
    def __init__(self, path):
        self.path = Path.cwd() / Path('test_data/').joinpath(path)


class TestFilesWorker:
    @pytest.mark.parametrize('path, err', [
        ['not existing folder', ObjectNotFoundException],
        ['folder_without_docs_files', DocsFileNotFoundError],
        ['not_a_folder', DocsFileNotFoundError],
        ['not_markdown_file.txt', DocsFileNotFoundError],
    ])
    def test_folder_errors(self, path, err):
        with pytest.raises(err):
            FilesWorker(SettingsMock(path)).get_files()
