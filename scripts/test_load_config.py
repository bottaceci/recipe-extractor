import yaml
from pathlib import Path

from recipe_extractor.config.loaders import load_yaml_config

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "ingredient_seq2seq.yaml"

def main() -> None:
    config = load_yaml_config(CONFIG_PATH)

    print(f"Model name: {config["model"]["name"]} | Train path: {config["data"]["train_path"]} | Output dir: {config["training"]["output_dir"]}")

if __name__ == "__main__":
    main()