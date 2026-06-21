# Recipe Extractor

## Overview

Recipe Extractor is a machine learning and data engineering project that extracts structured recipe information from raw recipe webpages.

The project began as a deterministic extraction pipeline and evolved into a hybrid system combining:

* HTML parsing
* Structured storage in a relational database
* Dataset generation pipelines
* Sequence-to-sequence machine learning models
* LLM-assisted dataset curation

The long-term goal is to build a robust recipe database that can ingest recipes from multiple websites and automatically extract searchable ingredients and recipe metadata.

---

## Future Work

### Data Collection

* Scrape additional recipe websites
* Increase ingredient diversity
* Expand training dataset

### Model Improvements

* Larger sequence-to-sequence models
* Improved evaluation metrics
* Error analysis tooling
* Experiment tracking

### Application Layer

Planned features:

* Ingredient search interface
* Recipe recommendation
* Interactive recipe browser
* Manual correction workflows

### LLM-Assisted Workflows

* Human-reviewed normalization cache
* Interactive ingredient correction
* Incremental dataset improvement

---

## Current Pipeline

```text
Website Discovery
        ↓
HTML Download
        ↓
HTML Archive
        ↓
Deterministic Extraction
        ↓
Ingredient Normalization
        ↓
Processed Dataset Generation
        ↓
Database Population
```

---

## Current Features

### Recipe Discovery

The application can automatically discover recipe URLs from supported websites.

Currently supported:

* Two Plaid Aprons
* Healthy Simple Yum

### HTML Archiving

Downloaded recipe pages are stored locally to:

* enable offline processing
* create reproducible datasets
* support future machine learning experiments

### Deterministic Recipe Extraction

The deterministic extractor parses recipe pages and extracts:

* Recipe title
* Ingredients
* Quantities
* Units
* Instructions
* Metadata

The extracted data is stored as structured JSON records and can be loaded into a relational database.

### Ingredient Normalization

The project supports multiple normalization strategies:

#### Deterministic Normalizer

Rule-based normalization using handcrafted cleaning rules.

Removes:

* Preparation instructions
* Punctuation
* Common noise words
* Formatting artifacts

#### LLM-Assisted Normalizer

Uses a local instruction-tuned language model (`Qwen2.5-1.5B-Instruct`) to generate cleaned ingredient names.

Features:

* Local execution
* No paid API required
* Caching of previous normalizations
* Optional human review and correction
* Fully reproducible after cache generation

---

## Project Structure

```text
recipe-extractor/
├── README.md
├── config
│   └── ingredient_seq2seq.yaml
├── data
│   ├── cache
│   │   └── ingredient_normalization_llm.json
│   ├── exports
│   │   ├── extraction_debug.csv
│   │   └── ingredient_dataset_debug.csv
│   ├── metadata.jsonl
│   └── processed
│       ├── deterministic
│       └── llm
├── legacy
│   ├── app.py
│   ├── create_database.py
│   ├── database_functions.py
│   ├── models.py
│   ├── query.py
│   ├── recipe_scraper.zip
│   ├── recipes.db
│   ├── scraping_functions.py
│   └── website-list.txt
├── main.py
├── project_structure.txt
├── pyproject.toml
├── scripts
│   ├── 0_download_pages.py
│   ├── 1_build_pipeline.py
│   ├── 2_model_pipeline.py
│   ├── build_ingredient_dataset.py
│   ├── build_ingredient_seq2seq_dataset.py
│   ├── build_processed_dataset.py
│   ├── debug_extractor.py
│   ├── evaluate_ingredient_parser.py
│   ├── inspect_ingredient_dataset.py
│   ├── load_database.py
│   ├── split_ingredient_seq2seq_dataset.py
│   ├── test_ingredient_inference.py
│   ├── test_load_config.py
│   ├── test_parser.py
│   ├── test_qwen_normalizer.py
│   ├── test_save_recipe.py
│   ├── test_tokenization.py
│   └── train_ingredient_parser.py
├── src
│   └── recipe_extractor
│       ├── __init__.py
│       ├── config
│       │   ├── __init__.py
│       │   └── loaders.py
│       ├── data
│       │   ├── __init__.py
│       │   └── schemas.py
│       ├── extraction
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── deterministic.py
│       │   └── exceptions.py
│       ├── ml
│       │   ├── __init__.py
│       │   ├── dataset.py
│       │   ├── evaluation.py
│       │   ├── inference.py
│       │   ├── schemas.py
│       │   └── training.py
│       ├── normalization
│       │   ├── __init__.py
│       │   ├── cache.py
│       │   ├── deterministic.py
│       │   └── llm.py
│       ├── scraping
│       │   ├── __init__.py
│       │   ├── discovery.py
│       │   └── downloader.py
│       ├── services
│       │   └── __init__.py
│       └── storage
│           ├── __init__.py
│           ├── database.py
│           ├── models.py
│           └── repositories.py
├── tests
└── uv.lock
```

---

## Technologies

* Python
* BeautifulSoup
* Requests
* SQLAlchemy
* SQLite
* Pydantic
* Pandas
* Scikit-Learn
* PyTorch
* Hugging Face Transformers
* Local LLMs

---

## Project Architecture

```text
raw_html/
    ↓
build_processed_dataset
    ↓
recipes.jsonl
    ↓
load_database
    ↓
SQLite database
    ↓
build_ingredient_dataset
    ↓
ingredients.jsonl
    ↓
build_ingredient_seq2seq_dataset
    ↓
ingredient_seq2seq.jsonl
    ↓
split_ingredient_seq2seq_dataset
    ↓
train / validation / test datasets
    ↓
T5 training
    ↓
evaluation
```

---

## Dataset Pipeline

The dataset pipeline is fully automated.

```bash
uv run python scripts/build_pipeline.py \
    --normalizer deterministic \
    --dataset-name deterministic
```

or

```bash
uv run python scripts/build_pipeline.py \
    --normalizer llm \
    --dataset-name llm
```

The pipeline:

1. Builds processed recipe records
2. Creates the SQLite database
3. Creates the ingredient dataset
4. Creates the seq2seq dataset
5. Splits the dataset by recipe

Recipes are split by recipe URL to avoid ingredient leakage between train and test sets.

---

## Database

The SQLite database contains:

### Recipes

Stores recipe-level information.

### Ingredients

Stores unique ingredient names.

### RecipeIngredients

Many-to-many relationship between recipes and ingredients.

Stores:

* Raw ingredient HTML
* Quantity
* Unit
* Ingredient reference

Recipe search is performed using partial matching rather than strict equality.

This preserves information while still enabling flexible ingredient searches.

---

## Deterministic Results

Using deterministic extraction:

* 200 recipe pages processed
* 194 recipes successfully stored
* 787 unique normalized ingredients
* 2119 recipe-ingredient relationships

The extraction pipeline currently achieves greater than 99% successful parsing on the collected sample set.

---

## Machine Learning

### Ingredient Parsing Model

The ingredient parser is trained as a sequence-to-sequence task.

Input:

```html
<li class="wprm-recipe-ingredient">
    ...
</li>
```

Output:

```json
{
  "name": "granulated sugar",
  "normalized_name": "granulated sugar",
  "quantity": 0.5,
  "unit": "cup"
}
```

### Model

Current model:

```text
google-t5/t5-small
```

Fine-tuned on the generated ingredient dataset.

---

## Evaluation

Evaluation is performed on a held-out test set.

Metrics:

* Valid JSON generation
* Ingredient name accuracy
* Normalized ingredient accuracy
* Unit accuracy
* Quantity accuracy
* Full-record accuracy

Latest results:
| Metric                | Score |
| --------------------- | ----- |
| Valid JSON            | 99.2% |
| Name Match            | 94.0% |
| Normalized Name Match | 84.9% |
| Unit Match            | 99.2% |
| Quantity Match        | 98.4% |
| All Fields Match      | 83.3% |

## Roadmap

### Phase 1 — Deterministic Extraction

* [x] URL discovery
* [x] HTML download
* [x] HTML archiving
* [x] Recipe extraction
* [x] Ingredient normalization
* [x] Database storage

### Phase 2 — Dataset Generation

* [X] Ingredient parsing dataset
* [X] Recipe extraction dataset
* [X] Dataset quality evaluation

### Phase 3 — Machine Learning

* [X] Ingredient parsing model
* [ ] Recipe extraction model
* [ ] Model evaluation framework

### Phase 4 — LLM Experiments

* [X] LLM-assisted ingredient normalization
* [ ] LLM-based recipe extraction
* [ ] Deterministic vs ML vs LLM comparison

### Phase 5 — Desktop Application

* [ ] Search interface
* [ ] Ingredient filtering
* [ ] Recipe browsing
* [ ] Database management

---

## Status

🚧 Active Development

The deterministic extraction pipeline is operational and the project is currently transitioning toward dataset generation and machine learning experimentation.

The ML model can reliably parse all ingredient attributes and compute the normalized ingredient name starting from the relative HTML snippet.

Developement has stopped for now. The method of extraction of the information, starting from the raw HTML page, is not optimal, and may structural scripts can be improved upon. A new *Recipe Extractor* project was started, using a multi classifier model on the recipe text instead of parsing the HTML.
