from datasets import Dataset, DatasetDict
import json
from transformers import AutoTokenizer
from transformers import (
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

def load_seq2seq_dataset(config: dict) -> DatasetDict:

    with open(config["data"]["train_path"], 'r') as f:
        train_set = [json.loads(line) for line in f]
    with open(config["data"]["val_path"], 'r') as f:
        val_set = [json.loads(line) for line in f]
    with open(config["data"]["test_path"], 'r') as f:
        test_set = [json.loads(line) for line in f]

    output = DatasetDict({
        "train": Dataset.from_list(train_set),
        "validation": Dataset.from_list(val_set),
        "test": Dataset.from_list(test_set),
    })

    return output

def load_tokenizer(config: dict):
    return AutoTokenizer.from_pretrained(config["model"]["name"])

def tokenize_seq2seq_dataset(
        dataset: DatasetDict,
        tokenizer,
        config: dict
) -> DatasetDict:
    max_input_length = config["training"]["max_input_length"]
    max_target_length = config["training"]["max_target_length"]

    def preprocess_function(examples):
        model_inputs = tokenizer(
            examples["input"],
            max_length = max_input_length,
            truncation = True
        )

        labels = tokenizer(
            text_target=examples["target"],
            max_length=max_target_length,
            truncation=True,
        )

        model_inputs["labels"] = labels["input_ids"]

        return model_inputs
    
    tokenized_dataset = dataset.map(
        preprocess_function,
        batched = True,
        remove_columns=dataset["train"].column_names,
    )

    return tokenized_dataset

def load_model(config: dict):
    return AutoModelForSeq2SeqLM.from_pretrained(config["model"]["name"])


def get_data_collator(tokenizer, model):
    return DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
    )

def build_training_args(config: dict) -> Seq2SeqTrainingArguments:
    training_config = config["training"]

    return Seq2SeqTrainingArguments(
        output_dir=training_config["output_dir"],
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=float(training_config["learning_rate"]),
        per_device_train_batch_size=int(training_config["batch_size"]),
        per_device_eval_batch_size=int(training_config["batch_size"]),
        num_train_epochs=int(training_config["num_train_epochs"]),
        predict_with_generate=True,
        logging_steps=20,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        use_cpu=True,
    )

def build_trainer(
    model,
    training_args,
    tokenized_dataset,
    tokenizer,
    data_collator,
) -> Seq2SeqTrainer:
    return Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        processing_class=tokenizer,
        data_collator=data_collator,
    )
