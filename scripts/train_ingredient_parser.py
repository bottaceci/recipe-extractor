from pathlib import Path

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


def main() -> None:
    config = load_yaml_config(CONFIG_PATH)

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
    trainer.train()

    output_dir = config["training"]["output_dir"]

    print(f"Saving model to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    print("Training complete.")


if __name__ == "__main__":
    main()