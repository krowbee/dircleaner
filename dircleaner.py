from send2trash import send2trash
from dataclasses import dataclass, field
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent


@dataclass 
class Config:
    path: Path = field(default=BASE_DIR / "config.json")

    def __post_init__(self):
        if not self.path.is_file():
            raise FileNotFoundError("File not exists")
        
        self.data = json.loads(self.path.read_text(encoding="utf-8"))
        raw = self.data.get("dirs_to_clean", [])
        items = raw if isinstance(raw, (list, tuple)) else [raw]
        self.dirs_to_clean = [Path(p).expanduser() for p in items if p]


class DirCleaner:

    def __init__(self, config: Config):
        self.config = config

    def clean_dirs(self):
        counter = 0
        for d in self.config.dirs_to_clean:

            if not d.exists():
                print(f"Skip {d}. does not exists")
                continue

            if not d.is_dir():
                print(f"Skip {d}. not a directory")
                continue

            if d == Path("/") or d == Path.home():
                print("Skip dangerous directory")
                continue

            for file in d.iterdir():
                if file.is_file() or file.is_dir():
                    counter += 1
                    send2trash(file)
        print(f"{counter} files was removed")


if __name__ == "__main__":
    config = Config()
    dircleaner = DirCleaner(config)
    dircleaner.clean_dirs()
