from pathlib import Path
import shutil
import json

from recipe_extractor.config.loaders import load_yaml_config
from recipe_extractor.ml.training import (
    build_trainer,
    build_training_args,
    get_data_collator,
    load_model,
    load_seq2seq_dataset,
    load_tokenizer,
    tokenize_seq2seq_dataset,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "ingredient_seq2seq.yaml"


def main(config_path: Path) -> None:
    config = load_yaml_config(config_path)

    output_dir = Path(config["training"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(config_path, output_dir / "training_config.yaml")

    print("Loading dataset...")
    dataset = load_seq2seq_dataset(config)

    print("Loading tokenizer and model...")
    tokenizer = load_tokenizer(config)
    model = load_model(config)

    print("Tokenizing dataset...")
    tokenized_dataset = tokenize_seq2seq_dataset(dataset, tokenizer, config)

    print("Preparing trainer...")
    data_collator = get_data_collator(tokenizer, model)
    training_args = build_training_args(config)

    trainer = build_trainer(
        model=model,
        training_args=training_args,
        tokenized_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    print("Starting training...")
    train_result = trainer.train()

    print("Starting evaluation...")
    eval_metrics = trainer.evaluate()

    metrics = {
        "train": train_result.metrics,
        "eval": eval_metrics,
    }

    print(f"Saving model and metrics to {output_dir}...")
    with open(output_dir / "train_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with open(output_dir / "log_history.json", "w", encoding="utf-8") as f:
        json.dump(trainer.state.log_history, f, indent=2)

    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    print("Training complete.")


if __name__ == "__main__":
    main(config_path=CONFIG_PATH)