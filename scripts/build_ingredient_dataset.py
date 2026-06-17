from pathlib import Path
import json

def main(output_dir: Path) -> None:
    dataset_path = output_dir / "recipes.jsonl"
    output_path = output_dir / "ingredients.jsonl"

    if output_path.exists():
        output_path.unlink()

    with open(dataset_path) as f:
        samples = [json.loads(line) for line in f]

    with open(output_path, "a", encoding="utf-8") as f:
        for sample in samples:
            ingredients = sample.get("recipe", {}).get("ingredients") if sample.get("recipe") else None
            if ingredients:
                for ingredient in ingredients:
                    record = {
                        "recipe_url": sample["url"],
                        "source": sample["source"],
                        "input_html": ingredient["raw_text"],
                        "quantity": ingredient["quantity"],
                        "unit": ingredient["unit"],
                        "name": ingredient["name"],
                        "normalized_name": ingredient["normalized_name"]
                    }

                    f.write(json.dumps(record) + "\n")

if __name__ == "__main__":
    main()
