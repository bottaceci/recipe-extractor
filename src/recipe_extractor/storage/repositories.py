from sqlalchemy.orm import Session

from recipe_extractor.data.schemas import RecipeData
from recipe_extractor.storage.models import Recipe, Ingredient, RecipeIngredient

def save_recipe(session: Session, recipe_data: RecipeData) -> Recipe:
    existing_recipe = (
        session.query(Recipe)
        .where(Recipe.url == recipe_data.url)
        .first()
    )

    # If the recipe is present, return it
    if existing_recipe:
        return existing_recipe
    
    # If the recipe is not present, insert it in the database
    recipe = Recipe(
        title = recipe_data.title,
        url = recipe_data.url,
        source = recipe_data.source,
        total_time = recipe_data.total_time,
        thumbnail_url = recipe_data.thumbnail_url
    )

    session.add(recipe)

    for ing_data in recipe_data.ingredients:
        ingredient = (
            session.query(Ingredient)
            .where(Ingredient.normalized_name == ing_data.normalized_name)
            .first()
        )

        if ingredient is None:
            ingredient = Ingredient(
                name = ing_data.name,
                normalized_name = ing_data.normalized_name
            )
            session.add(ingredient)

        # When dealing with newly created ORM objects, connect objects through relationships, not IDs.
        recipe_ingredient = RecipeIngredient(
            recipe = recipe,
            ingredient = ingredient,
            raw_text = ing_data.raw_text,
            quantity = ing_data.quantity,
            unit = ing_data.unit 
        )

        session.add(recipe_ingredient)

    return recipe


