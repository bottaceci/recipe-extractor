# This module contains the function that normalizes the ingredient names
import re

DESCRIPTORS_TO_REMOVE = [
    "fresh", "dried", "ground", "minced", "chopped", "grated", "peeled", "kosher", 
    "fine", "coarse", "large", "small", "medium", "optional", "extra", "virgin",
    "white", "yellow", "roasted", "diced", "warm",
]

UNITS_TO_REMOVE = [
    "knob", "pinch", "pat",
]

OTHERS_TO_REMOVE = [
    "of", "a", "or", "and",
]

def normalize_ingredient(ing_name: str) -> str:
    # Apply lowercase
    ing = ing_name.lower()

    # Remove punctuation
    ing = re.sub("[().,;:\-–]", '', ing)

    # Remove numbers
    ing = re.sub('[1234567890]', '', ing)

    # Remove known descriptors
    for desc in DESCRIPTORS_TO_REMOVE:
        ing = re.sub(rf"\b{re.escape(desc)}\b", "", ing)

    # Remove known units
    for desc in UNITS_TO_REMOVE:
        ing = re.sub(rf"\b{re.escape(desc)}\b", "", ing)

    # Remove known others
    for desc in OTHERS_TO_REMOVE:
        ing = re.sub(rf"\b{re.escape(desc)}\b", "", ing)

    # Remove eventual leading and trailing whitespaces
    ing = ing.lstrip()
    ing = ing.rstrip()

    # Get singular

    return ing

def amount_convertor(amount: str) -> float:
    try:
        amount = float(amount)
    except:
        if amount == '1½':
            amount = 1.5
        if amount == '⅓':
            amount = 0.33
        if amount == '½':
            amount = 0.5
        if amount == '¼':
            amount = 0.25

    return amount