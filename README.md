# Recipe Extractor

## Status

🚧 **This project is currently under active development.**

The architecture, machine learning pipeline, and user interface are still evolving. Features and implementation details may change significantly before the first stable release.

---

## Overview

Recipe Extractor is a machine learning and data engineering project whose goal is to automatically extract structured recipe information from cooking websites.

The project originated from a previous application that relied on custom scraping logic for each supported website. While effective, that approach required writing and maintaining site-specific extraction rules whenever a new recipe source was added.

The objective of this project is to replace those deterministic rules with a generalized extraction system capable of identifying recipes from arbitrary webpages and converting them into a structured format suitable for storage, search, and analysis.

---

## Goals

The project explores multiple approaches to recipe extraction:

1. **Rule-Based Extraction**

   * Traditional handcrafted scraping utilities.
   * Used as a baseline and data generation tool.

2. **Machine Learning Extraction**

   * Models trained on previously collected recipe data.
   * Automatic extraction of recipe fields from webpage content.

3. **LLM-Based Extraction**

   * Large Language Models used to generate structured recipe representations.
   * Compared against custom-trained models in terms of accuracy, speed, cost, and maintainability.

---

## Dataset

The training dataset is built from previously collected recipes and consists of:

* Raw webpage content
* Cleaned webpage text
* Structured recipe labels

Each recipe is represented as a structured object containing information such as:

* Title
* Ingredients
* Quantities
* Units
* Preparation time
* Source website
* Recipe instructions
* Images and metadata

---

## Database

Recipes are stored in a relational database using SQLAlchemy.

Core entities include:

* Recipes
* Ingredients
* Recipe–Ingredient relationships

This structure enables advanced filtering capabilities, including:

* Search by recipe name
* Search by ingredient
* Search by source website
* Future support for tags, categories, and nutritional information

---

## Project Structure

```text
recipe-extractor/
│
├── config/
├── data/
│   ├── raw_html/
│   ├── processed/
│   ├── exports/
│   └── models/
│
├── notebooks/
├── tests/
│
└── src/
    └── recipe_extractor/
        ├── config/
        ├── scraping/
        ├── extraction/
        ├── storage/
        ├── services/
        ├── data/
        └── ml/
```

---

## Technology Stack

* Python
* SQLAlchemy
* BeautifulSoup
* Pandas
* Pydantic
* SQLite
* PyTorch (planned)
* Hugging Face Transformers (planned)
* Flet (planned)

Package management is handled through **uv**.

---

## Roadmap

### Phase 1 — Foundation

* [x] Legacy scraper analysis
* [x] Database migration planning
* [ ] New backend architecture
* [ ] Dataset generation pipeline

### Phase 2 — Data Collection

* [ ] Webpage acquisition
* [ ] HTML storage
* [ ] Dataset construction
* [ ] Data validation

### Phase 3 — Machine Learning

* [ ] Baseline extraction model
* [ ] Training pipeline
* [ ] Evaluation framework
* [ ] Error analysis

### Phase 4 — LLM Comparison

* [ ] Prompt-based extraction
* [ ] Structured JSON generation
* [ ] Cost and performance evaluation

### Phase 5 — Application

* [ ] Desktop user interface
* [ ] Database browsing
* [ ] Recipe search
* [ ] Dataset refresh workflow
* [ ] New website onboarding

---

## Motivation

This project serves both as a practical utility and as a demonstration of end-to-end machine learning development.

It combines:

* Data collection
* Data modeling
* Natural language processing
* Information extraction
* Database design
* Model evaluation
* Application development

The long-term objective is to build a system capable of transforming unstructured recipe webpages into a searchable and maintainable recipe database with minimal manual intervention.
