from pathlib import Path
import pandas as pd

from recipe_extractor.config.loaders import load_yaml_config
from recipe_extractor.ml.training import (
    load_seq2seq_dataset,
)
from recipe_extractor.ml.inference import (
    load_model,
    load_tokenizer,
    predict_ingredient,
)
from recipe_extractor.ml.evaluation import (
    evaluate_prediction,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "data" / "models" / "t5_ingredient_parser_5ep" / "training_config.yaml"

metric_columns = [
    "valid_json",
    "name_match",
    "normalized_name_match",
    "soft_normalized_name_match",
    "unit_match",
    "quantity_match",
    "all_fields_match",
]


def main() -> None:
    config = load_yaml_config(CONFIG_PATH)

    output_dir = Path(config["training"]["output_dir"])

    print("Loading dataset...")
    dataset = load_seq2seq_dataset(config)
    test_dataset = dataset["test"]

    print("Loading tokenizer and model...")
    tokenizer = load_tokenizer(config)
    model = load_model(config)

    print("Starting evaluation...")
    rows = []

    for i in range(len(test_dataset)):
        input_html = test_dataset["input"][i]
        target_text = test_dataset["target"][i]
        prediction_text = predict_ingredient(
            input_html=input_html,
            model=model,
            tokenizer=tokenizer,
            config=config
        )

        metrics = evaluate_prediction(prediction_text, target_text)

        row = {
            "input": input_html,
            "target": target_text,
            "prediction": prediction_text,
        }

        row.update(metrics)

        rows.append(row)

        if (i + 1) % 25 == 0:
            rows_df = pd.DataFrame(rows)
            print(rows_df[metric_columns].mean())
    
    rows_df = pd.DataFrame(rows)
    print(rows_df[metric_columns].mean())
    rows_df.to_csv(output_dir / "ingredient_parser_evaluation.csv", index=False)

    print("Evaluation complete.")


if __name__ == "__main__":
    main()