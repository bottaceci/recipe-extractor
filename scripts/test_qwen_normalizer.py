from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map=None,
)
model.to("cpu")
model.eval()

def main(ing: str):
    # Create message
    messages = [
        {
            "role": "system",
            "content": (
                "You normalize recipe ingredient names. "
                "Return only the canonical ingredient name in lowercase singular. "
                "Remove punctuation, size, quantity, packaging, preparation, texture, and processing descriptors. "
                "Preserve descriptors that define a distinct ingredient type, variety, species, or culinary category. "
                #"Singularize. "
            ),
        },
        {
            "role": "user",
            "content": (
                f"Normalize this ingredient name: {ing}\n\n"
                "Examples:\n"
                "Kosher salt -> salt\n"
                "granulated sugar -> sugar\n"
                "ground cinnamon -> cinnamon\n"
                "napa cabbage -> napa cabbage\n"
                "brown sugar -> brown sugar\n"
                "whole milk -> milk\n"
                "extra virgin olive oil -> olive oil"
            ),
        },
    ]

    # Apply the chat template
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    # Tokenize
    inputs = tokenizer(
        [text],
        return_tensors="pt",
    )
    # To CPU
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # Generate
    generated_ids = model.generate(
        **inputs,
        max_new_tokens=32,
        do_sample=False,
    )

    # Decode only new tokens
    new_tokens = generated_ids[0][inputs["input_ids"].shape[-1]:]

    output = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True,
    ).strip()

    return output