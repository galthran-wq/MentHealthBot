from pathlib import Path
import yaml

base_path = Path(__file__).parent.parent


def load_yaml(name: str):
    path = base_path / name
    with path.open() as f:
        return yaml.safe_load(f)


config = load_yaml('config/config.yml')
