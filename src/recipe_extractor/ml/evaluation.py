import json

def parse_prediction(text: str) -> dict | None:
    if not text.strip().startswith("{"):
        text = "{" + text
    if not text.strip().endswith("}"):
        text = text + "}"

    try:
        text_dict = json.loads(text)
    except json.JSONDecodeError:
        return None
    
    return text_dict

def compare_quantity(pred: dict, target: dict) -> bool:
    pred_quantity = pred.get("quantity")
    target_quantity = target.get("quantity")

    if pred_quantity is None and target_quantity is None:
        return True

    if pred_quantity is None or target_quantity is None:
        return False

    return abs(float(pred_quantity) - float(target_quantity)) <= 1e-6

def normalize_text_for_comparison(value: str | None) -> str | None:
    if value is None:
        return None

    return " ".join(value.lower().strip().split())

def compare_field(pred: dict, target: dict, field: str) -> bool:
    pred_value = normalize_text_for_comparison(pred.get(field))
    target_value = normalize_text_for_comparison(target.get(field))

    return pred_value == target_value

def canonicalize_ingredient_name(value: str | None) -> str | None:
    value = normalize_text_for_comparison(value)

    if value is None:
        return None

    if value.endswith("ies"):
        return value[:-3] + "y"

    if value.endswith("es"):
        return value[:-2]

    if value.endswith("s") and not value.endswith("ss"):
        return value[:-1]

    return value

def compare_normalized_name_soft(pred: dict, target: dict) -> bool:
    return (
        canonicalize_ingredient_name(pred.get("normalized_name"))
        == canonicalize_ingredient_name(target.get("normalized_name"))
    )

def evaluate_prediction(prediction_text, target_text) -> dict:
    prediction = parse_prediction(prediction_text)
    target = parse_prediction(target_text)

    metrics = {
        "valid_json": False,
        "name_match": False,
        "normalized_name_match": False,
        "soft_normalized_name_match": False,
        "unit_match": False,
        "quantity_match": False,
    }

    if prediction is None or target is None:
        metrics["all_fields_match"] = False
        return metrics
    
    metrics["valid_json"] = True

    metrics["name_match"] = compare_field(prediction, target, "name")

    metrics["normalized_name_match"] = compare_field(prediction, target, "normalized_name")

    metrics["soft_normalized_name_match"] = compare_normalized_name_soft(prediction, target)

    metrics["unit_match"] = compare_field(prediction, target, "unit")

    metrics["quantity_match"] = compare_quantity(prediction, target)

    metrics["all_fields_match"] = (
        metrics["valid_json"]
        and metrics["name_match"]
        and metrics["soft_normalized_name_match"]
        and metrics["unit_match"]
        and metrics["quantity_match"]
    )

    return metrics
