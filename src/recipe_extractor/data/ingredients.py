# This module contains the function that normalizes the ingredient names
import re

DESCRIPTORS_TO_REMOVE = [
    "fresh", "dried", "ground", "minced", "chopped", "grated", "peeled", "kosher", 
    "fine", "coarse", "large", "small", "medium", "optional", "extra", "virgin",
    "white", "yellow", "roasted", "diced", "warm", "regular", "all-purpose",
    "allpurpose", "cooked", "black", "granulated", "crushed", "cut",
]

UNITS_TO_REMOVE = [
    "knob", "pinch", "pat", "to taste", "can", "cans", "packet", "package",
    "loaf", "cups", "cloves"
]

OTHERS_TO_REMOVE = [
    "of", "a", "or", "and", "&", "see above", "your choice", "few cracks"
]

def normalize_ingredient(ing_name: str) -> str:
    # Apply lowercase
    ing = ing_name.lower()

    # Remove punctuation
    ing = re.sub("[().,;:–-]", '', ing)

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

    # Remove eventual double spaces
    ing = re.sub(r"\s+", " ", ing)

    return ing

def amount_convertor(amount: str) -> float:
    try:
        return float(amount)
    except ValueError:
        pass

    fractions = {
        '1½': 1.5,
        '1 ½': 1.5,
        '⅓': 1 / 3,
        '½': 0.5,
        '¼': 0.25,
        '¾': 0.75,
        '⅔': 2 / 3,
        '⅛': 0.125,
        '1¼': 1.25,
        '1¾': 1.75,
        '2½': 2.5,
        '8 ½': 8.5,
        '4¼': 4.25,
        '2¼': 2.25,
        '⅙': 1 / 6,
        '1⅓': 1 + 1 / 3,
        '2⅓': 2 + 1 / 3,
        '3¼': 3.25 ,
        '1 ¼': 1.25,
    }

    amount = amount.strip()

    if amount in fractions:
        return fractions[amount]

    m = re.fullmatch(r"\s*(\d+)(?:[¼½¾⅓⅔⅛⅜⅝⅞])?\s*[-–—]\s*(\d+)", amount)
    if m:
        return float(m.group(1))

    raise ValueError(f"Cannot convert amount: {amount!r}")
        

    return amount