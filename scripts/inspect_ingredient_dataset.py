from pathlib import Path
from collections import Counter
import pandas as pd

from recipe_extractor.ml.dataset import load_ingredient_samples


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "ingredients.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "data" / "exports" / "ingredient_dataset_debug.csv"


def main() -> None:
    samples = load_ingredient_samples(DATASET_PATH)

    samples_df = pd.DataFrame([s.__dict__ for s in samples])

    total_rows = samples_df.shape[0]
    missing_input_html = samples_df["input_html"].isna().sum()
    missing_name = samples_df["name"].isna().sum()
    missing_normalized_name = samples_df["normalized_name"].isna().sum()
    missing_quantity = samples_df["quantity"].isna().sum()
    missing_unit = samples_df["unit"].isna().sum()

    n_unique_raw_ings = samples_df["name"].nunique()
    n_unique_ings = samples_df["normalized_name"].nunique()
    ings_rank = samples_df["normalized_name"].value_counts()
    units_rank = samples_df["unit"].value_counts()

    print(f"""
        Total rows: {total_rows}
        Missing input_html: {missing_input_html}
        Missing name: {missing_name}
        Missing normalized_name: {missing_normalized_name}
        Missing quantity: {missing_quantity}
        Missing unit: {missing_unit}
        Unique normalized ingredients: {n_unique_ings}

        Top 30 normalized ingredients: {ings_rank.head(30)}
        Top 30 units: {units_rank.head(30)}

    """)

    print(ings_rank.describe())
    print(ings_rank[ings_rank >= 5].shape[0])
    print(ings_rank[ings_rank >= 10].shape[0])
    print(ings_rank[ings_rank == 1].shape[0])
    print(n_unique_raw_ings)

    pd.DataFrame(samples_df).to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()