from pathlib import Path
import json
from sqlalchemy import func, select

from recipe_extractor.storage.database import get_engine, get_session, create_tables
from recipe_extractor.storage.repositories import save_recipe
from recipe_extractor.data.schemas import RecipeData
from recipe_extractor.storage.models import Recipe, Ingredient, RecipeIngredient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "test_recipes.db"
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "recipes.jsonl"

engine = get_engine(DB_PATH)
create_tables(engine=engine)

session = get_session(engine=engine)

with open(DATASET_PATH) as f:
    samples = [json.loads(line) for line in f]

for i,sample in enumerate(samples, start=1):
    if sample["status"] != "ok":
        continue

    print(f"[{i}/{len(samples)}] Loading {sample['html_path']}")

    recipe = RecipeData.model_validate(sample["recipe"])
    _ = save_recipe(session=session, recipe_data=recipe)

session.commit()

recipe_count = session.scalar(select(func.count()).select_from(Recipe))
ingredient_count = session.scalar(select(func.count()).select_from(Ingredient))
recipe_ingredient_count = session.scalar(
    select(func.count()).select_from(RecipeIngredient)
)

print(f"Recipes: {recipe_count}")
print(f"Ingredients: {ingredient_count}")
print(f"Recipe ingredients: {recipe_ingredient_count}")
