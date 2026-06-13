# Recipe Extractor

## Overview

Recipe Extractor is a Python application designed to automatically collect, parse, normalize, and store recipes from cooking websites.

The project originated as a rule-based recipe scraper, but is being redesigned as a platform for experimenting with machine learning and information extraction techniques. The long-term goal is to compare deterministic scraping, machine learning models, and LLM-based approaches for extracting structured recipe data from raw HTML pages.

The project is currently in active development.

---

## Goals

### Immediate Goals

* Discover recipe pages from supported websites
* Download and archive raw HTML pages
* Extract structured recipe information
* Normalize ingredient names and quantities
* Store recipes in a searchable database

### Long-Term Goals

* Build supervised datasets for recipe extraction tasks
* Train machine learning models to parse ingredient information
* Train models to extract recipes directly from web pages
* Compare deterministic extraction against ML and LLM approaches
* Provide a desktop application for recipe search and management

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

Recipes are extracted from raw HTML into a unified schema.

Extracted information includes:

* recipe title
* source URL
* source website
* total preparation time
* thumbnail image
* ingredients
* ingredient quantities
* ingredient units

### Ingredient Normalization

Ingredient names are normalized to improve searchability and reduce duplicates.

Examples:

```text
Kosher salt        → salt
Fresh ginger       → ginger
Knob of ginger     → ginger
Ground pepper      → pepper
```

### Database Storage

Recipes are stored in a SQLite database using SQLAlchemy.

Current schema:

```text
recipes
ingredients
recipe_ingredients
```

This allows querying recipes by ingredient and supports future filtering capabilities.

---

## Project Structure

```text
recipe-extractor/
│
├── data/
│   ├── raw_html/
│   ├── processed/
│   └── metadata.jsonl
│
├── scripts/
│   ├── download_pages.py
│   ├── debug_extractor.py
│   ├── build_processed_dataset.py
│   └── load_database.py
│
├── src/
│   └── recipe_extractor/
│       ├── data/
│       ├── extraction/
│       ├── scraping/
│       └── storage/
│
└── tests/
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

Planned:

* Scikit-Learn
* PyTorch
* Hugging Face Transformers
* Local LLMs

---

## Dataset Generation

The project generates structured datasets from downloaded recipe pages.

Current dataset:

```text
HTML page
↓
RecipeData object
↓
JSONL dataset
```

This dataset will serve as the foundation for future machine learning experiments.

---

## Current Results

Using deterministic extraction:

* 200 recipe pages processed
* 194 recipes successfully stored
* 787 unique normalized ingredients
* 2119 recipe-ingredient relationships

The extraction pipeline currently achieves greater than 99% successful parsing on the collected sample set.

---

## Roadmap

### Phase 1 — Deterministic Extraction

* [x] URL discovery
* [x] HTML download
* [x] HTML archiving
* [x] Recipe extraction
* [x] Ingredient normalization
* [x] Database storage

### Phase 2 — Dataset Generation

* [ ] Ingredient parsing dataset
* [ ] Recipe extraction dataset
* [ ] Dataset quality evaluation

### Phase 3 — Machine Learning

* [ ] Ingredient parsing model
* [ ] Recipe extraction model
* [ ] Model evaluation framework

### Phase 4 — LLM Experiments

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
