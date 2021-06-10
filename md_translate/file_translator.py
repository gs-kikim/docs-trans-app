from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, List

from md_translate.line_processor import Line
from md_translate.logs import logger

if TYPE_CHECKING:
    from md_translate.settings import Settings


class FileTranslator:
    default_open_mode: str = 'r+'
    default_write_mode: str = 'w'
    default_encoding: str = 'utf8'

    def __init__(self, settings: 'Settings', file_path: Path, copy_path: Path) -> None:
        self.settings = settings
        self.file_path: Path = file_path
        self.copy_path: Path = copy_path
        self.file_contents_with_translation: list = []
        self.code_block: bool = False

    def __enter__(self) -> 'FileTranslator':
        self.__r_translating_file: IO = self.file_path.open(self.default_open_mode, encoding=self.default_encoding)
        self.__w_translating_file: IO = self.copy_path.open(self.default_write_mode, encoding=self.default_encoding)
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.__r_translating_file.close()
        self.__w_translating_file.close()

    def leave_original_translate(self) -> None:
        lines = self._get_lines()
        for counter, _line in enumerate(lines):
            line = Line(self.settings, _line)
            self.file_contents_with_translation.append(line.original)
            self.code_block = (
                not self.code_block if line.is_code_block_border() else self.code_block
            )
            if line.can_be_translated() and not self.code_block:
                self.file_contents_with_translation.append('\n')
                self.file_contents_with_translation.append(line.fixed)
                logger.info(f'Processed {counter+1} lines')
        self._write_translated_data_to_file()

    #  TODO 1. ** 강조 ** 한칸 띄어지는 문제, (**, >)
    #  TODO 3. 뒷 문장이 제대로 작성 안되는 문제 (<br>)
    def erase_original_translate(self) -> None:
        lines = self._get_lines()
        for counter, _line in enumerate(lines):
            line = Line(self.settings, _line)
            self.code_block = (
                not self.code_block if line.is_code_block_border() else self.code_block
            )
            if line.can_be_translated() and not self.code_block:
                self.file_contents_with_translation.append(line.fixed)
                logger.info(f'Processed {counter+1} lines')
            else:
                self.file_contents_with_translation.append(line.original)
        self._write_translated_data_to_file()

    def _get_lines(self) -> List[str]:
        lines = self.__r_translating_file.readlines()
        logger.info(f'Got {len(lines)} lines to process')
        return lines

    def _write_translated_data_to_file(self) -> None:
        self.__w_translating_file.seek(0)
        self.__w_translating_file.writelines(self.file_contents_with_translation)
