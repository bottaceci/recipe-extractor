import argparse
from pathlib import Path

from build_processed_dataset import main as build_processed_dataset
from load_database import main as load_database
from build_ingredient_dataset import main as build_ingredient_dataset
from build_ingredient_seq2seq_dataset import main as build_ingredient_seq2seq_dataset
from split_ingredient_seq2seq_dataset import main as split_ingredient_seq2seq_dataset

from recipe_extractor.normalization.deterministic import normalize_ingredient as deterministic_normalizer
from recipe_extractor.normalization.llm import normalize_ingredient as llm_normalizer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE_PATH = PROJECT_ROOT / "data" / "cache" / "ingredient_normalization_llm.json"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--normalizer",
        choices=["deterministic","llm"],
        default="deterministic",
    )
    parser.add_argument(
        "--dataset-name",
        default="deterministic",
    )

    group = parser.add_argument_group("Normalizer arguments", description='''
Normalizer arguments. Available:
    --review-normalization
    --cache-path''')
    group.add_argument(
        "--review-normalization",
        action="store_true"
    )
    group.add_argument(
        "--cache-path",
        default=DEFAULT_CACHE_PATH
    )
    return parser.parse_args()

def get_normalizer(name: str):
    if name == "deterministic":
        return deterministic_normalizer
    if name == 'llm':
         return llm_normalizer

    raise ValueError(f"Unknown normalizer: {name}")

def get_output_dir(name: str):
    return PROJECT_ROOT / "data" / "processed" / name

def get_normalizer_args(args):
        return {
             "review": args.review_normalization,
             "cache_path": args.cache_path
        }

def main() -> None:
    args = parse_args()
    normalizer = get_normalizer(args.normalizer)
    output_dir = get_output_dir(args.dataset_name)
    normalizer_args = get_normalizer_args(args)
    print(f"Using normalizer: {args.normalizer}")
    print(f"Output directory: {output_dir}")
    print(f"Normalizer arguments: {normalizer_args}")

    print("Building processed recipe dataset...")
    build_processed_dataset(normalizer=normalizer, output_dir=output_dir, normalizer_args=normalizer_args)

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