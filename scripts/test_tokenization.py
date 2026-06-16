from pathlib import Path

from recipe_extractor.config.loaders import load_yaml_config
from recipe_extractor.ml.training import (
    load_tokenizer,
    load_seq2seq_dataset,
    tokenize_seq2seq_dataset,
    load_model,
    get_data_collator,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "ingredient_seq2seq.yaml"


def main() -> None:
    config = load_yaml_config(CONFIG_PATH)

    dataset = load_seq2seq_dataset(config)
    tokenizer = load_tokenizer(config)

    tokenized_dataset = tokenize_seq2seq_dataset(dataset, tokenizer, config)

    print(tokenized_dataset)
    print(tokenized_dataset["train"][0].keys())
    print(tokenizer.decode(tokenized_dataset["train"][0]["input_ids"]))
    print(tokenizer.decode(tokenized_dataset["train"][0]["labels"]))

    model = load_model(config)
    data_collator = get_data_collator(tokenizer, model)

    print(type(model))
    print(type(data_collator))

if __name__ == "__main__":
    main()