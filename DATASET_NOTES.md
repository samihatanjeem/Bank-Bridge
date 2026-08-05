# Dataset Notes (for Person A)

The datasets in `/data` are currently **dummy placeholders** — small,
illustrative, and marked `"source_notes": "DUMMY DATA"`. Replace them with
real, sourced data before the demo.

## financial_products.json — schema

Each entry needs:

| Field | What goes here |
|---|---|
| `id` | Unique short identifier, e.g. `bd_fdr` |
| `country` | Origin country name, or `"United States"` for US reference products |
| `product_name_local` | Full product name |
| `local_terms` | List of alternate names/abbreviations a user might type |
| `description` | 1-2 sentence plain description of what the product is |
| `key_features` | List of notable features (tenure, minimums, rates, etc.) |
| `closest_us_equivalent` | Best-match US product name (or note if there's no clean match) |
| `similarity_notes` | What's genuinely similar to the US equivalent |
| `difference_notes` | What's genuinely different — this is the most valuable field, be specific |
| `source_notes` | Where this came from (bank name, government site, etc.) |

## account_opening_process.json — schema

| Field | What goes here |
|---|---|
| `country` | Country name |
| `process_name` | Label for this process |
| `steps` | Ordered list of steps to open the account |
| `typical_requirements` | List of documents/requirements needed |
| `notes` | Anything worth flagging to the user (digital vs. in-person norms, etc.) |
| `source_notes` | Where this came from |

## Where to find real data

- **Bank product pages directly** — most banks publish savings/deposit
  product pages with features, minimums, and rates
- **Central bank / government sites** — e.g. Bangladesh Bank, RBI (India),
  BSP (Philippines) often publish official product category info
- **FDIC.gov** — good source for US-side definitions and insurance details
- Avoid forums/aggregator sites where possible; prefer the bank's own page or
  a government source so you can cite it confidently if a judge asks

## Reminder

Double check any number you plan to say out loud in the demo video —
interest rates and minimums change, and a wrong number stated on camera is an
easy, avoidable mistake.
