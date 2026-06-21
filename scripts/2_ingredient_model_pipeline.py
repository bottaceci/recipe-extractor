import argparse
from pathlib import Path

from train_ingredient_parser import main as train_ingredient_parser
from evaluate_ingredient_parser import main as evaluate_ingredient_parser

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = "config/ingredient_seq2seq.yaml"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-path",
        default=DEFAULT_CONFIG_PATH,
    )
    parser.add_argument(
        "--evaluation-only",
        action="store_true"
    )
    return parser.parse_args()

def get_config_path(name: str):
    return PROJECT_ROOT / name

def main() -> None:
    args = parse_args()
    config_path = get_config_path(args.config_path)
    print(f"Using configuration from {str(config_path)}")

    if not args.evaluation_only:
        print("Starting training...")
        train_ingredient_parser(config_path=config_path)

    print("Starting evaluation...")
    evaluate_ingredient_parser(config_path=config_path)

if __name__ == "__main__":
    main()