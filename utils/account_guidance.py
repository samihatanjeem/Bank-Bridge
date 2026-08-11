"""Account-type-specific guidance layered onto each country's base process."""

from typing import Dict, List


ACCOUNT_TYPES: Dict[str, dict] = {
    "Checking / current account": {
        "category": "transactions",
        "plain_name": "checking or current account",
        "purpose": "For salary deposits, card purchases, bills, and transfers.",
        "compare": "monthly fees, minimum balances, ATM access, transfer options, and overdraft rules",
        "decision": "Choose your overdraft preference and confirm which debit-card, transfer, and bill-pay tools are included.",
    },
    "Savings account": {
        "category": "savings",
        "plain_name": "savings account",
        "purpose": "For accessible savings that may earn interest.",
        "compare": "the interest rate, minimum balance, fees, withdrawal access, and deposit protection",
        "decision": "Choose how you will fund the account and set up an optional recurring transfer from your spending account.",
    },
    "High-yield savings (HYSA)": {
        "category": "savings",
        "plain_name": "high-yield savings account",
        "purpose": "For accessible savings where the advertised return is a priority.",
        "compare": "the current annualized rate, whether it is variable, minimums, fees, withdrawal speed, and deposit protection",
        "decision": "Link a funding account, make a small test transfer, and confirm how quickly withdrawals reach you.",
        "notice": "“High-yield” is a marketing description, not a universal account category. The local product name and how rates are quoted vary by country.",
    },
    "Fixed-term deposit / CD": {
        "category": "fixed_term",
        "plain_name": "fixed-term deposit or certificate of deposit",
        "purpose": "For a lump sum you can leave untouched until a chosen maturity date.",
        "compare": "term length, fixed return, minimum deposit, early-withdrawal consequences, tax treatment, and renewal rules",
        "decision": "Choose the term and maturity instructions before funding; save the confirmation and maturity date.",
    },
    "Basic / low-cost account": {
        "category": "basic_account",
        "plain_name": "basic or low-cost account",
        "purpose": "For essential deposits and payments with simpler or lower-cost features.",
        "compare": "eligibility, monthly cost, included transactions, balance limits, card access, and overdraft availability",
        "decision": "Confirm which essential services are included and which transactions or balances may be limited.",
    },
}


def account_type_options() -> List[str]:
    return list(ACCOUNT_TYPES)


def account_profile(account_type: str) -> dict:
    return ACCOUNT_TYPES[account_type]


def tailored_steps(process: dict, account_type: str, local_product_name: str) -> List[str]:
    """Add product-specific decisions to a country's reviewed onboarding flow."""
    profile = account_profile(account_type)
    base_steps = process.get("steps", []) if process else []
    onboarding_steps = base_steps[1:] if base_steps else []
    decision_index = next(
        (
            index
            for index, step in enumerate(onboarding_steps)
            if "fund" in step.lower() or "deposit" in step.lower()
        ),
        max(len(onboarding_steps) - 1, 0),
    )
    onboarding_steps.insert(decision_index, profile["decision"])
    return [
        f"Compare {local_product_name} options: {profile['compare']}.",
        *onboarding_steps,
    ]
