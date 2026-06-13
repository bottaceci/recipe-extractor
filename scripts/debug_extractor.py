from pathlib import Path
import pandas as pd
import json

from recipe_extractor.extraction.deterministic import DeterministicRecipeExtractor
from recipe_extractor.data.schemas import RecipeData

metadata_path = Path("data/metadata.jsonl")
output_path = Path("data/exports/extraction_debug.csv")

output_path.parent.mkdir(parents=True, exist_ok=True)

extractor = DeterministicRecipeExtractor()
with open(metadata_path) as f:
    metadata_records = [json.loads(line) for line in f]
rows = []

for metadata in metadata_records:
    try:
        html = Path(metadata["html_path"]).read_text(encoding="utf-8")
        recipe: RecipeData = extractor.extract(html, metadata["url"])

        for ingredient in recipe.ingredients:
            rows.append({
                "source": metadata.get("source"),
                "url": metadata.get("url"),
                "title": recipe.title,
                "total_time": recipe.total_time,
                "thumbnail_present": recipe.thumbnail_url is not None,
                "raw_ingredient": ingredient.raw_text,
                "ingredient_name": ingredient.name,
                "normalized_name": ingredient.normalized_name,
                "quantity": ingredient.quantity,
                "unit": ingredient.unit,
                "status": "ok",
                "error": None,
            })

    except Exception as exc:
        rows.append({
            "source": metadata.get("source"),
            "url": metadata.get("url"),
            "title": None,
            "total_time": None,
            "thumbnail_present": None,
            "raw_ingredient": None,
            "ingredient_name": None,
            "normalized_name": None,
            "quantity": None,
            "unit": None,
            "status": "error",
            "error": str(exc),
        })

pd.DataFrame(rows).to_csv(output_path, index=False)