from pathlib import Path
import json

from recipe_extractor.ml.dataset import load_ingredient_samples


def main(output_dir: Path) -> None:
    dataset_path = output_dir / "ingredients.jsonl"
    output_path = output_dir / "ingredient_seq2seq.jsonl"

    if output_path.exists():
        output_path.unlink()
        
    samples = load_ingredient_samples(dataset_path)

    with open(output_path, "w", encoding="utf-8") as f:
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