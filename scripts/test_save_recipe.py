from pathlib import Path

from recipe_extractor.storage.database import get_engine, get_session, create_tables
from recipe_extractor.data.schemas import RecipeData, IngredientData
from recipe_extractor.storage.repositories import save_recipe
from recipe_extractor.storage.models import Recipe

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "test_recipes.db"

engine = get_engine(DB_PATH)
create_tables(engine=engine)

session = get_session(engine=engine)

rec = RecipeData(
    title="Hot Chocolate",
    url="cookingblog.com",
    source="Cooking Blog",
    total_time=10,
    ingredients=[
        IngredientData(
            name="Cocoa",
            normalized_name="cocoa",
            raw_text="Cocoa",
            quantity=30,
            unit="g"
        ),
        IngredientData(
            name="Milk",
            normalized_name="milk",
            raw_text="Milk",
            quantity=250,
            unit="ml"
        )
    ]
)

recipe = save_recipe(session=session, recipe_data=rec)

session.commit()

queried_rec = session.query(Recipe).where(Recipe.title == recipe.title).first()
queried_ingredients = [ing.ingredient.name for ing in queried_rec.recipe_ingredients]

print(f"Title: {queried_rec.title} | Ingredients: {queried_ingredients}")

