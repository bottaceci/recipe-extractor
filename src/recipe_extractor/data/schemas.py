from pydantic import BaseModel

class IngredientData(BaseModel):
    name: str
    normalized_name: str
    raw_text: str
    quantity: float | None = None
    unit: str | None = None

class RecipeData(BaseModel):
    title: str
    url: str
    source: str
    total_time: int | None = None
    thumbnail_url: str | None = None
    ingredients: list[IngredientData]