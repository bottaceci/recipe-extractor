from pathlib import Path

from recipe_extractor.config.loaders import load_yaml_config
from recipe_extractor.ml.training import (
    load_seq2seq_dataset,
)
from recipe_extractor.ml.inference import (
    load_model,
    load_tokenizer,
    predict_ingredient,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "training_config.yaml"


def main() -> None:
    config = load_yaml_config(CONFIG_PATH)

    print("Loading dataset...")
    dataset = load_seq2seq_dataset(config)

    print("Loading tokenizer and model...")
    tokenizer = load_tokenizer(config)
    model = load_model(config)

    print("Starting inference...")
    # Pick 5 random elements from the test dataset
    examples = dataset["test"][:5]
    for i in range(5):
        input_html = examples["input"][i]
        target = examples["target"][i]
        prediction = predict_ingredient(
            input_html=input_html,
            model=model,
            tokenizer=tokenizer,
            config=config
        )

        if not prediction.strip().startswith("{"):
            prediction = "{" + prediction
        if not prediction.strip().endswith("}"):
            prediction = prediction + "}"

        print(f"""
    SAMPLE {i}
    INPUT:
    {input_html}

    TARGET:
    {target}

    PREDICTION:
    {prediction}

    =================================
        """)
    

    print("Inference complete.")


if __name__ == "__main__":
    main()