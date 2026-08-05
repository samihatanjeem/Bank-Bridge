# Bank Bridge

Understand your money the moment you land.

Bank Bridge helps newcomers translate their home country's financial products
and account-opening process into their closest US equivalent, and translates
bank statements for visa/loan/apartment applications.

Built for [Hackathon Name] — Financial Inclusion track (with Newcomer
Settlement crossover).

## Status

🚧 Early build. Front-end pages work against a **dummy dataset** with a
rule-based placeholder explanation. Real AI calls and verified data are not
wired up yet — see the TODOs below.

## Project structure

```
bank-bridge/
├── Home.py                        # Main app entry point / landing page
├── pages/
│   ├── 1_Term_Translator.py       # Financial product lookup + explanation
│   ├── 2_Process_Comparison.py    # Account-opening process comparison
│   └── 3_Statement_Translator.py  # Bank statement upload + translation (stub)
├── utils/
│   ├── data_loader.py             # JSON loading + lookup helpers
│   └── ai_helper.py                # AI explanation logic (placeholder for now)
├── data/
│   ├── financial_products.json    # Dummy dataset — REPLACE before demo
│   └── account_opening_process.json  # Dummy dataset — REPLACE before demo
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

1. Clone the repo and `cd` into it.
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template and add your API key (only needed once
   `ai_helper.py` is wired up to a real model — the app runs fine without it
   for now, using the placeholder explanations):
   ```bash
   cp .env.example .env
   ```
5. Run the app:
   ```bash
   streamlit run Home.py
   ```
   This opens the app in your browser at `http://localhost:8501`.

## Team split (Day 1)

**Person A — Data**
- Expand `data/financial_products.json` and `data/account_opening_process.json`
  with real, sourced data (5-8 products per country)
- Keep the existing schema (see field descriptions in each JSON file's
  sibling notes, or ask in Slack if unclear)
- You can edit these files directly — no need to touch any Python code to
  add more entries; the app reads them automatically

**Person B — AI integration**
- Open `utils/ai_helper.py` — look for the `TODO` comments in
  `explain_product()` and `explain_statement()`
- Wire up a real Claude or OpenAI API call, using the existing
  `_fallback_explanation()` and `_build_prompt()` functions as a starting
  template
- The front-end already calls these functions correctly — you shouldn't need
  to touch any Streamlit page code, just the functions inside this file

**Both of you can work at the same time without blocking each other** —
Person A edits JSON files, Person B edits `ai_helper.py`, and the Streamlit
pages already wire both together.

## Known gaps / next steps

- [ ] Replace dummy data with verified data (see `DATASET_NOTES.md` for
      sourcing guidance)
- [ ] Wire up real LLM calls in `ai_helper.py`
- [ ] Wire up the Statement Translator to a vision-capable model call
- [ ] Add more countries beyond Bangladesh/India/Philippines if time allows
- [ ] Add a disclaimer banner (informational only, not financial advice) —
      currently only in page captions, consider making more prominent
- [ ] Deploy to Streamlit Community Cloud for a live demo link

## Disclaimer

This tool is for informational and educational purposes only. It does not
constitute financial, legal, or immigration advice. Data is currently a
development placeholder and has not been fully verified for accuracy.
