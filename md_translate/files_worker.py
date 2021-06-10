from pathlib import Path
from typing import TYPE_CHECKING, Iterable
import shutil

from md_translate.exceptions import FileIsNotMarkdown, ObjectNotFoundException

if TYPE_CHECKING:
    from md_translate.settings import Settings


class FilesWorker:
    suffix = ['.md', '.rst']

    def __init__(self, settings: 'Settings') -> None:
        self.settings = settings
        self.single_file: bool = False
        self.object_to_process: Path = self.settings.path
        self.__check_for_single_obj()
        self.__validate_folder()

    def __check_for_single_obj(self) -> None:
        if self.object_to_process.is_file() and self.object_to_process.suffix in self.suffix:
            self.single_file = True
        elif self.object_to_process.is_file():
            raise FileIsNotMarkdown(self.object_to_process)

    def __validate_folder(self) -> None:
        if not self.object_to_process.exists():
            raise ObjectNotFoundException(self.object_to_process)

    def get_files(self) -> Iterable[Path]:
        files_list: list = []
        if self.single_file:
            files_list.append(self.object_to_process)
        else:
            files_list.extend(
                [
                    link
                    for link in self.object_to_process.iterdir()
                    if link.suffix in self.suffix
                ]
            )
        if len(files_list) == 0:
            raise FileNotFoundError('There are no MD or RST files found with provided path!')

        return files_list

    def copy_files(self, path: Iterable[Path]) -> Iterable[Path]:
        files_list: list = []
        target_dir = self.settings.target_dir

        for src in path:
            try:
                dst = target_dir / src.name
                shutil.copyfile(src, dst)
            except Exception as err:
                raise Exception("[ERROR] Failed to copy:" + str(dst) + "\n" + err)
            else:
                files_list.append(dst)

        return files_list

    def create_file(self, src: Path) -> Path:
        target_dir = self.settings.target_dir / src.name

        try:
            open(file=target_dir, mode='x').close()
        except FileExistsError:
            pass
        except Exception as err:
            raise Exception("[ERROR] Failed to create:" + str(target_dir) + "\n" + err)

        return target_dir


