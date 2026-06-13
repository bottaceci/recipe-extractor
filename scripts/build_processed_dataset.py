from pathlib import Path
import json

from recipe_extractor.extraction.deterministic import DeterministicRecipeExtractor

metadata_path = Path("data/metadata.jsonl")
output_path = Path("data/processed/recipes.jsonl")

output_path.parent.mkdir(parents=True, exist_ok=True)

if output_path.exists():
    output_path.unlink()

extractor = DeterministicRecipeExtractor()
with open(metadata_path) as f:
    metadata_records = [json.loads(line) for line in f]
rows = []

with open(output_path, "a", encoding="utf-8") as f:
    for metadata in metadata_records:
        try:
            html = Path(metadata["html_path"]).read_text(encoding="utf-8")
            recipe = extractor.extract(html, metadata["url"])

            record = {
                "url": metadata["url"],
                "source": metadata["source"],
                "html_path": metadata["html_path"],
                "recipe": recipe.model_dump(),
                "status": "ok",
                "error": None,
            }

        except Exception as exc:
            record = {
                "url": metadata["url"],
                "source": metadata["source"],
                "html_path": metadata["html_path"],
                "recipe": None,
                "status": "error",
                "error": str(exc),
            }

        
        f.write(json.dumps(record) + "\n")