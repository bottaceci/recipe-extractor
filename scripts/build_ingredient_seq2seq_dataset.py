from pathlib import Path
import json

from recipe_extractor.ml.dataset import load_ingredient_samples


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "ingredients.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "ingredient_seq2seq.jsonl"

if OUTPUT_PATH.exists():
    OUTPUT_PATH.unlink()

def main() -> None:
    samples = load_ingredient_samples(DATASET_PATH)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for sample in samples:
            target_obj = {
                "quantity": sample.quantity,
                "unit": sample.unit,
                "name": sample.name,
                "normalized_name": sample.normalized_name,
            }

            record = {
                "input": sample.input_html,
                "recipe_url": sample.recipe_url,
                "source": sample.source,
                "target": json.dumps(target_obj, ensure_ascii=False, sort_keys=True),
            }

            f.write(json.dumps(record) + "\n")

if __name__ == "__main__":
    main()