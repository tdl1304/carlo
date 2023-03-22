import os
from pathlib import Path


def confirm_path_overwrite(path: Path):
    if os.path.exists(path):
        overwrite = input("File already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() == "n":
            exit()