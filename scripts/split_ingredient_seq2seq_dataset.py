from sklearn.model_selection import train_test_split
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "ingredient_seq2seq.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed"

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f]

recipe_urls = sorted({record["recipe_url"] for record in records})

train_urls, temp_urls = train_test_split(
    recipe_urls,
    test_size=0.2,
    random_state=42,
)

val_urls, test_urls = train_test_split(
    temp_urls,
    test_size=0.5,
    random_state=42,
)

train_urls = set(train_urls)
val_urls = set(val_urls)
test_urls = set(test_urls)

train_records = [r for r in records if r["recipe_url"] in train_urls]
val_records = [r for r in records if r["recipe_url"] in val_urls]
test_records = [r for r in records if r["recipe_url"] in test_urls]

with open(OUTPUT_PATH / "ingredient_seq2seq_train.jsonl", 'w') as f:
    for record in train_records:
        f.write(json.dumps(record) + "\n")

with open(OUTPUT_PATH / "ingredient_seq2seq_val.jsonl", 'w') as f:
    for record in val_records:
        f.write(json.dumps(record) + "\n")

with open(OUTPUT_PATH / "ingredient_seq2seq_test.jsonl", 'w') as f:
    for record in test_records:
        f.write(json.dumps(record) + "\n")

# print(f"Train recipes: {len(train_urls)} | Val recipes: {len(val_urls)} | Test recipes: {len(test_urls)}")
# print(f"Train rows: {len(train_records)} | Val rows: {len(val_records)} | Test rows: {len(test_records)}")

# print(f"Total ingredient rows: {len(records)}")
# print(f"Unique recipe URLs in ingredient dataset: {len(recipe_urls)}")