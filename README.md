# BankBridge Passport

Your financial history should not reset at the border.

BankBridge turns a fictional or redacted financial document into a
privacy-minimized evidence profile and a sourced 30-day financial-access plan.
It helps newcomers carry understandable evidence across borders without
creating a black-box credit score or eligibility decision.

## The working MVP

- Multimodal document analysis for PDFs and images through the OpenAI Responses API
- Strict structured extraction that omits names and account identifiers
- Explainable evidence signals with confidence labels and redaction warnings
- A destination-specific account pathway, document checklist, and 30-day plan
- A downloadable Financial Passport containing no direct identity fields
- A zero-data fictional demo that remains usable without an API key
- Supporting product translation and account-opening tools across 11 markets

## Status

The Passport, term, and process pages use sourced seed data for 10 origin countries plus
the United States as a destination market:
Bangladesh, China, the Dominican Republic, El Salvador, India, Mexico, the
Philippines, South Korea, the United Kingdom, and Vietnam. Free-text mapping
uses an explainable hybrid matcher with fuzzy aliases, product mechanics,
intent cues, and a multinomial Naive Bayes signal. Low-confidence inputs fall
back safely. Users can select any covered market other than their home country
as the destination. The account-opening guide provides tailored checklists for
everyday spending, savings, high-yield savings, fixed-term, and basic accounts.

The Passport is deliberately not an alternative credit score. It organizes
evidence and preparation steps; institutions remain responsible for their own
verification, eligibility, and lending decisions.

## Project structure

```text
bank-bridge/
├── Home.py
├── pages/
│   ├── 1_Term_Translator.py
│   ├── 2_Process_Comparison.py
│   └── 3_Financial_Passport.py
├── utils/
│   ├── account_guidance.py
│   ├── data_loader.py
│   ├── passport.py
│   └── product_classifier.py
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

The fictional Passport demo works immediately. To enable AI document analysis,
set `OPENAI_API_KEY` in the environment or in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-key-here"
```

`OPENAI_MODEL` optionally overrides the default `gpt-5.4-mini` model. Uploaded
files are sent directly as base64 inputs to the Responses API with `store=False`;
the application does not write them to disk. Use synthetic or properly redacted
documents for demonstrations. See the official OpenAI documentation for
[file inputs](https://developers.openai.com/api/docs/guides/file-inputs),
[vision](https://developers.openai.com/api/docs/guides/images-vision), and
[Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

## Test

```bash
python -m unittest discover -s tests -v
```

The term translator trains from the small JSON dataset at runtime, so there is no opaque
serialized model artifact. It combines fuzzy name matching, Unicode-aware
lexical similarity, explicit product-mechanics cues, and Naive Bayes trained on
names, aliases, descriptions, and stable features. A reviewed canonical
category then routes the result to the closest product in the chosen
destination. The UI links both sides of each result back to their evidence.

See `DATASET_NOTES.md` before adding records or categories.
See `HACKATHON_SUBMISSION.md` for the elevator pitch, three-minute demo script,
technical story, disclosure, and impact metrics.

## AI workflow

```text
redacted document
       ↓
vision / file understanding
       ↓
strict privacy-minimized schema
       ↓
deterministic pathway engine + reviewed country data
       ↓
cited 30-day plan + downloadable Passport
```

The AI extracts document evidence. Deterministic application code then connects
that evidence to reviewed destination requirements. This separation prevents
the model from inventing account-opening rules or making financial decisions.

## Hackathon build disclosure

The original foundation included the Streamlit shell, product translator, and
account-process comparison. The Financial Passport, multimodal document
workflow, strict extraction schema, privacy controls, evidence presentation,
30-day plan, synthetic demo, and Passport tests were built as the substantive
hackathon extension.

## Known gaps

- The seed mappings need domain-expert review before production use.
- Coverage is a curated seed set rather than a complete catalog of each market.
- Model confidence is a routing heuristic, not a calibrated probability.
- Live document extraction requires an OpenAI API key and has not been validated
  for use with real customer financial data.

## Disclaimer

This tool is for informational and educational purposes only. It is not a
credit score, lending decision, eligibility determination, or financial, legal,
tax, or immigration advice. Mappings are functional analogies and do not
establish identical legal, insurance, tax, or contractual treatment.
