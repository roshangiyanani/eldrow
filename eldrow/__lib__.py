from pathlib import Path
from typing import Sequence


def load_words(path: Path) -> Sequence[str]:
    return path.read_text().splitlines()
