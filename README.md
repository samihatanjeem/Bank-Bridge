# Bank Bridge

Understand your money the moment you land.

BankBridge helps newcomers translate financial-product terms and compare
account-opening processes across 11 destination markets. It also provides a
privacy-first guide for understanding and safely sharing bank statements.

## Status

The term and process pages use sourced seed data for 10 origin countries plus
the United States as a destination market:
Bangladesh, China, the Dominican Republic, El Salvador, India, Mexico, the
Philippines, South Korea, the United Kingdom, and Vietnam. Free-text mapping
uses an explainable hybrid matcher with fuzzy aliases, product mechanics,
intent cues, and a multinomial Naive Bayes signal. Low-confidence inputs fall
back safely. Users can select any covered market other than their home country
as the destination.

## Project structure

```text
bank-bridge/
├── Home.py
├── pages/
│   ├── 1_Term_Translator.py
│   ├── 2_Process_Comparison.py
│   └── 3_Statement_Guide.py
├── utils/
│   ├── data_loader.py
│   ├── product_classifier.py
│   └── ai_helper.py
├── data/
│   ├── financial_products.json
│   ├── additional_financial_products.json
│   ├── account_opening_process.json
│   └── additional_account_opening_process.json
├── tests/
└── DATASET_NOTES.md
```

## Setup

Requires Python 3.9 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Home.py
```

## Test

```bash
python -m unittest discover -s tests -v
```

The model trains from the small JSON dataset at runtime, so there is no opaque
serialized model artifact. It combines fuzzy name matching, Unicode-aware
lexical similarity, explicit product-mechanics cues, and Naive Bayes trained on
names, aliases, descriptions, and stable features. A reviewed canonical
category then routes the result to the closest product in the chosen
destination. The UI links both sides of each result back to their evidence.

See `DATASET_NOTES.md` before adding records or categories.

## Known gaps

- The seed mappings need domain-expert review before production use.
- The statement guide validates file readiness but does not read or translate documents.
- Coverage is a curated seed set rather than a complete catalog of each market.
- Model confidence is a routing heuristic, not a calibrated probability.

## Disclaimer

This tool is for informational and educational purposes only. It does not
constitute financial, legal, tax, or immigration advice. Mappings are
functional analogies and do not establish identical legal, insurance, tax, or
contractual treatment.
