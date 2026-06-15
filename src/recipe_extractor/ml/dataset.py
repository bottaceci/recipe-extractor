from pathlib import Path
import json

from recipe_extractor.ml.schemas import IngredientSample


def load_ingredient_samples(path: Path) -> list[IngredientSample]:
    samples: list[IngredientSample] = []

    with open(path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                raw_sample = json.loads(line)
                sample = IngredientSample.model_validate(raw_sample)
                samples.append(sample)
            except Exception as exc:
                raise ValueError(
                    f"Invalid ingredient sample at line {line_number}: {line}"
                ) from exc

    return samples