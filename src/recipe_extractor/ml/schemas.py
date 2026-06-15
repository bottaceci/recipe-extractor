from pydantic import BaseModel


class IngredientSample(BaseModel):
    recipe_url: str
    source: str
    input_html: str
    quantity: float | None
    unit: str | None
    name: str
    normalized_name: str