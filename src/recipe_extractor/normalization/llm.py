import re
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM

from recipe_extractor.normalization.cache import (
    get_cached_normalization,
    set_cached_normalization,
    load_cache,
    save_cache,
)

### OLD
NORMALIZATION_INSTRUCTIONS = """
Normalize the recipe ingredient name.
Return only the canonical ingredient name in lowercase.

Examples:
Kosher salt -> salt
granulated sugar -> sugar
medium apples -> apple
ground cinnamon -> cinnamon
napa cabbage -> napa cabbage
brown sugar -> brown sugar
whole milk -> milk
extra virgin olive oil -> olive oil
"""
LOCAL_NORMALIZER_MODEL = "google/flan-t5-base"
MAX_INPUT_LENGTH = 256
MAX_OUTPUT_LENGTH = 32

# tokenizer = AutoTokenizer.from_pretrained(LOCAL_NORMALIZER_MODEL)
# model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_NORMALIZER_MODEL)
# model.eval()

### CURRENT
DEFAULT_CACHE_PATH = Path("data/cache/ingredient_normalization_llm.json")
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map=None,
)
model.to("cpu")
model.eval()

def build_prompt(name: str) -> str:
    return f"{NORMALIZATION_INSTRUCTIONS}\nIngredient: {name}\nNormalized:"

def call_llm(prompt: str) -> str:
    token_prompt = tokenizer(
        prompt,
        max_length=MAX_INPUT_LENGTH,
        truncation=True,
        return_tensors="pt",
    )

    generated_ids = model.generate(
        input_ids=token_prompt["input_ids"],
        attention_mask=token_prompt["attention_mask"],
        max_length=MAX_OUTPUT_LENGTH,
        do_sample=False,
        num_beams=1,
    )

    prediction = tokenizer.decode(
        generated_ids[0],
        skip_special_tokens=True,
    )

    return prediction

def clean_llm_output(raw: str, fallback_name: str) -> str:
    # lowercase and strip whitespace
    raw = raw.lower().strip()
    # remove quotes and punctuation
    raw = re.sub("[\"'().,;:–-]", " ", raw)
    # collapse repeated spaces
    final = " ".join(raw.split())

    if not final:
        return fallback_name.lower().strip()

    return final

def kwen_normalizer(ing: str):
    # Create message
    messages = [
        {
            "role": "system",
            "content": (
                "You clean recipe ingredient names for database search.\n"
                "\n"
                "Return only a cleaned ingredient name.\n"
                "Use lowercase text.\n"
                "Remove punctuation, measurement units, vague quantity words, and preparation notes.\n"
                "Remove words such as chopped, minced, diced, grated, peeled, sliced, optional, to taste.\n"
                "Remove connector noise such as 'of', 'and', 'or' only when it is not part of the ingredient name.\n"
                "Keep meaningful ingredient descriptors such as brown sugar, soy sauce, napa cabbage, sesame oil, olive oil.\n"
                "Keep the result close to the original ingredient name.\n"
                "Do not replace the ingredient with a broader category unless the removed word is only a preparation, size, or quantity descriptor.\n"
                "Do not explain your answer.\n"
                "\n"
                "Examples:\n"
                "knob of ginger -> ginger\n"
                "kosher salt -> kosher salt\n"
                "granulated sugar -> granulated sugar\n"
                "ground cinnamon -> cinnamon\n"
                "garlic cloves, minced -> garlic cloves\n"
                "medium apples -> apples\n"
                "big honeycrisp apples -> honeycrisp apples\n"
                "brown sugar -> brown sugar\n"
                "napa cabbage -> napa cabbage\n"
                "extra virgin olive oil -> extra virgin olive oil\n"
                "salt and pepper to taste -> salt pepper\n"
            ),
        },
        {
            "role": "user",
            "content": f"Clean this ingredient name:\n{ing}",
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

def review_normalization(name: str, proposed: str) -> str:
    print(f"\nIngredient: {name}")
    print(f"Proposed normalization: {proposed}")

    answer = input("Accept? [Y/n]: ").strip().lower()

    if answer in ("", "y", "yes"):
        return proposed

    if answer in ("n", "no"):
        corrected = input("Enter corrected normalization: ").strip().lower()
        corrected = clean_llm_output(corrected, fallback_name=name)
        return corrected

    print("Invalid input. Keeping proposed normalization.")
    return proposed

def normalize_ingredient(name: str, **kwargs) -> str:
    cache_path: Path = kwargs.get('cache_path', DEFAULT_CACHE_PATH)
    review: bool = kwargs.get("review", False)

    cache = load_cache(cache_path)

    cached = get_cached_normalization(name, cache)
    if cached:
        return cached

    ### Old model
    # prompt = build_prompt(name)
    # raw = call_llm(prompt)
    # normalized = clean_llm_output(raw, fallback_name=name)

    ### Kwen model
    raw = kwen_normalizer(name)
    normalized = clean_llm_output(raw, fallback_name=name)

    if review:
        normalized = review_normalization(name, normalized)

    set_cached_normalization(name, normalized, cache)
    save_cache(cache, cache_path)

    return normalized