# BankBridge Passport

## Elevator pitch

Newcomers arrive with years of financial history, but their documents and
banking language often do not travel with them. BankBridge Passport uses
multimodal AI to turn a redacted foreign financial document into an
explainable evidence profile and a sourced 30-day financial-access plan—without
creating a black-box credit score.

## The problem

A newcomer may have stable income, regular savings, and years of responsible
financial behavior while still appearing “new” to the destination system. The
immediate problem is not only missing credit data. It is also translation:
knowing which evidence is usable, what must be redacted, which local account
category to ask for, and what to do next.

## What the working product does

1. The user selects an origin, destination, and financial goal.
2. They use a fictional sample or provide a synthetic/redacted PDF or image.
3. AI extracts a strict privacy-minimized schema: document readiness, balance
   continuity, recurring-income pattern, broad obligation categories, and
   confidence-backed evidence notes.
4. Deterministic code connects that evidence to reviewed destination data.
5. The user receives local product terminology, required documents, redaction
   warnings, official sources, and a downloadable 30-day Financial Passport.

## Why the AI is substantive

- Vision and file understanding read layouts, tables, and financial text.
- Structured Outputs constrain extraction to an auditable schema.
- The prompt explicitly suppresses identity and account-number output.
- Confidence-backed evidence notes make every extracted signal inspectable.
- A deterministic policy layer prevents the model from inventing local rules.

The system does not wrap a chat completion in a generic chatbot. AI performs
document understanding; reviewed data and application code control the plan.

## Financial-inclusion boundary

BankBridge does not calculate creditworthiness, rank lenders, or make an
eligibility decision. That boundary avoids turning incomplete foreign evidence
into another opaque gatekeeping score. The Passport helps a person prepare and
communicate; the institution remains responsible for verification and decisions.

## Three-minute demo

**0:00–0:25 — Problem**  
“This person has years of financial history in India. In the US, that evidence
is hard to explain and easy to overshare.”

**0:25–0:55 — Inputs**  
Select India → United States → Open my first account. Show the fictional Naya
Bank statement and point out that no real personal data is needed.

**0:55–1:35 — AI extraction**  
Build the Passport. Show the document type, period, currency, readiness result,
evidence rows, confidence labels, and account-identifier warning. Emphasize that
the output contains no name or account number.

**1:35–2:15 — Action**  
Show the closest local pathway, destination document checklist, cited 30-day
plan, and official sources. Change the goal to emergency savings to demonstrate
that the pathway adapts.

**2:15–2:40 — Portability**  
Download the privacy-minimized Passport. Explain that it is an educational
preparation artifact, not a credit score or approval letter.

**2:40–3:00 — Scale**  
Show the 11 supported markets and the supporting term translator/account guide.
Close with: “Financial history should not reset at the border.”

## Technical stack

- Python 3.9+
- Streamlit
- OpenAI Responses API with vision/file inputs
- Strict JSON-schema Structured Outputs
- Explainable hybrid term classifier
- Curated regulator and first-party source records
- Standard-library deterministic planning and privacy filters

## Hackathon build disclosure

The original foundation included the Streamlit shell, term translator, and
account-process comparison. The Financial Passport, multimodal extraction,
strict schema, privacy controls, evidence experience, 30-day planning engine,
synthetic demo, download artifact, and Passport tests are the new hackathon
work.

## Impact metrics to measure next

- Time from first visit to a complete access plan
- Number of missing-document issues resolved before an application
- Percentage of users who complete at least one 30-day action
- Number of direct identifiers prevented from entering exported Passports
- User-reported confidence understanding destination banking terminology

## What comes next

- Multilingual Passport explanations and voice guidance
- Institution-maintained eligibility and document-requirement feeds
- On-device redaction before document transmission
- Human review through financial counselors and newcomer-serving nonprofits
- Formal extraction and fairness evaluations across document formats and markets
