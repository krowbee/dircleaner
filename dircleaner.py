from send2trash import send2trash
from dataclasses import dataclass
from pathlib import Path
import json
import argparse

BASE_DIR = Path(__file__).resolve().parent


@dataclass 
class Config:
    path: Path

    def __post_init__(self):
        self.path = self.path.expanduser()
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
                    send2trash(file)
                    counter += 1
        print(f"{counter} files was removed")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", type=Path, default=BASE_DIR / "config.json")
    args = parser.parse_args()

    config = Config(path=args.config)
    dircleaner = DirCleaner(config)
    dircleaner.clean_dirs()
