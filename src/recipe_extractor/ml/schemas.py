from pydantic import BaseModel


class IngredientSample(BaseModel):
    input_html: str
    quantity: float | None
    unit: str | None
    name: str
    normalized_name: str