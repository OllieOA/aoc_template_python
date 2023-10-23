# Example for relative common import

from pathlib import Path
from typing import List


class DataLoader:
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def load_data(self) -> List:
        with open(self.file_path, "r") as f:
            lines = [x.strip("\n") for x in f.readlines()]

        assert len(lines) > 0, "Did not load any data - check the file"
        return lines
