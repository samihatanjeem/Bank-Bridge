# Dataset Notes

The files in `/data` contain a compact reviewed seed set. The original three
markets and the seven-country expansion are split into base and `additional_`
JSON files for maintainability; the loader combines them. Each factual record
links to a regulator, government agency, or first-party bank page. Review the
links before production releases because products and regulations can change.

## `financial_products.json` and `additional_financial_products.json`

| Field | Meaning |
|---|---|
| `id` | Stable, unique record identifier |
| `country` | Origin country or `United States` for reference records |
| `product_name_local` | Full local product/category name |
| `local_terms` | Alternate terms and abbreviations used as training text |
| `description` | Plain description of the product mechanics |
| `key_features` | Stable characteristics used as training text |
| `closest_us_equivalent` | Reviewed classifier label |
| `similarity_notes` | Basis for the functional analogy |
| `difference_notes` | Material limits of the analogy |
| `sources` | Source objects containing `title` and direct `url` |

## Account-opening process files

`account_opening_process.json` and `additional_account_opening_process.json`
use the same schema. Each record contains a country, process label, ordered
steps, typical requirements, qualifications in `notes`, and a `sources` list.

## How the classifier uses the data

`utils/product_classifier.py` trains a multinomial Naive Bayes text classifier
at runtime. Names, aliases, descriptions, and key features are training text;
`closest_us_equivalent` is the label. Keeping them together means every model
output resolves to the reviewed evidence displayed in the UI.

Add varied aliases and stable mechanics rather than current rates. Every new
US-equivalent label should have examples in more than one country where
possible. Preserve “no direct standard equivalent” when a US analogy changes
the underlying contract.

## Source strategy

- Prefer central banks, regulators, deposit insurers, and official providers.
- Use provider pages for concrete product behavior and regulators for category
  definitions or rules.
- Avoid promotional rate claims unless an as-of date is displayed.
- Recheck every link and time-sensitive statement before release.
- Add classifier regression cases under `tests/` for new categories.

Run validation with:

```bash
python -m unittest discover -s tests -v
```
