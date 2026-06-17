from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def load_tokenizer(config: dict):
    return AutoTokenizer.from_pretrained(config["inference"]["model_path"])

def load_model(config: dict):
    model = AutoModelForSeq2SeqLM.from_pretrained(config["inference"]["model_path"])
    model.eval()
    return model

def predict_ingredient(input_html: str, model, tokenizer, config: dict) -> str:
    max_input_length = config["training"]["max_input_length"]
    max_target_length = config["training"]["max_target_length"]

    inputs = tokenizer(
        input_html,
        max_length=max_input_length,
        truncation=True,
        return_tensors="pt",
    )

    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_target_length,
    )

    prediction = tokenizer.decode(
        generated_ids[0],
        skip_special_tokens=True,
    )

    return prediction   