from pathlib import Path
from typing import TYPE_CHECKING, Iterable
import shutil

from md_translate.exceptions import FileIsNotMarkdown, ObjectNotFoundException

if TYPE_CHECKING:
    from md_translate.settings import Settings


class FilesWorker:
    suffixes = ['.md', '.rst']

    def __init__(self, settings: 'Settings') -> None:
        self.settings = settings
        self.single_file: bool = False
        self.object_to_process: Path = self.settings.path
        self.__check_for_single_obj()
        self.__validate_folder()

    def __check_for_single_obj(self) -> None:
        if self.object_to_process.is_file() and self.object_to_process.suffix in self.suffixes:
            self.single_file = True
        elif self.object_to_process.is_file():
            raise FileIsNotMarkdown(self.object_to_process)

    def __validate_folder(self) -> None:
        if not self.object_to_process.exists():
            raise ObjectNotFoundException(self.object_to_process)

    def get_files(self) -> Iterable[Path]:
        files_list: list = []
        for _suffix in self.suffixes:
            files_list.extend(self.object_to_process.glob('**/*'+_suffix))
        if len(files_list) == 0:
            raise FileNotFoundError('There are no MD or RST files found with provided path!')

        return files_list

    def create_file(self, src: Path) -> Path:
        sub_path = src.parts[len(self.object_to_process.parts):-1]
        target_dir = self.settings.target_dir / "\\".join(sub_path)

        try:
            if not target_dir.exists():
                target_dir.mkdir(exist_ok=True)
            target_file = target_dir / src.name
            if not target_file.exists():
                open(file=target_file, mode='x').close()
        except FileExistsError:
            pass
        except Exception as err:
            raise Exception("[ERROR] Failed to create:" + str(target_dir) + "\n" + err)

        return target_file


