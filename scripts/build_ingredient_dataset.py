from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "recipes.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "ingredients.jsonl"

if OUTPUT_PATH.exists():
    OUTPUT_PATH.unlink()

with open(DATASET_PATH) as f:
    samples = [json.loads(line) for line in f]

with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
    for sample in samples:
        ingredients = sample.get("recipe", {}).get("ingredients") if sample.get("recipe") else None
        if ingredients:
            for ingredient in ingredients:
                record = {
                    "input_html": ingredient["raw_text"],
                    "quantity": ingredient["quantity"],
                    "unit": ingredient["unit"],
                    "name": ingredient["name"],
                    "normalized_name": ingredient["normalized_name"]
                }

                f.write(json.dumps(record) + "\n")
