from pathlib import Path
import json
from sqlalchemy import func, select

from recipe_extractor.storage.database import get_engine, get_session, create_tables
from recipe_extractor.storage.repositories import save_recipe
from recipe_extractor.data.schemas import RecipeData
from recipe_extractor.storage.models import Recipe, Ingredient, RecipeIngredient

def main(output_dir: Path) -> None:
    dataset_path = output_dir / "recipes.jsonl"
    db_path = output_dir / "test_recipes.db"

    engine = get_engine(db_path)
    create_tables(engine=engine)

    session = get_session(engine=engine)

    with open(dataset_path) as f:
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

if __name__ == "__main__":
    main()
