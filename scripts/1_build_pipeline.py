import argparse
from pathlib import Path

from build_processed_dataset import main as build_processed_dataset
from load_database import main as load_database
from build_ingredient_dataset import main as build_ingredient_dataset
from build_ingredient_seq2seq_dataset import main as build_ingredient_seq2seq_dataset
from split_ingredient_seq2seq_dataset import main as split_ingredient_seq2seq_dataset
from recipe_extractor.normalization.deterministic import normalize_ingredient

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--normalizer",
        choices=["deterministic"],
        default="deterministic",
    )
    parser.add_argument(
        "--dataset-name",
        default="deterministic",
    )
    return parser.parse_args()

def get_normalizer(name: str):
    if name == "deterministic":
        return normalize_ingredient

    raise ValueError(f"Unknown normalizer: {name}")

def get_output_dir(name: str):
    return PROJECT_ROOT / "data" / "processed" / name

def main() -> None:
    args = parse_args()
    normalizer = get_normalizer(args.normalizer)
    output_dir = get_output_dir(args.dataset_name)
    print(f"Using normalizer: {args.normalizer}")
    print(f"Output directory: {output_dir}")

    print("Building processed recipe dataset...")
    build_processed_dataset(normalizer=normalizer, output_dir=output_dir)

    print("Loading database...")
    load_database(output_dir=output_dir)

    print("Building ingredient dataset...")
    build_ingredient_dataset(output_dir=output_dir)

    print("Building seq2seq dataset...")
    build_ingredient_seq2seq_dataset(output_dir=output_dir)

    print("Splitting seq2seq dataset...")
    split_ingredient_seq2seq_dataset(output_dir=output_dir)

if __name__ == "__main__":
    main()