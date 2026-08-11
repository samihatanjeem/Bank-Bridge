"""Small, explainable text classifier for cross-country product mappings.

The model is trained from the reviewed product records loaded from ``data/``
at runtime. This keeps training text and user-facing evidence together and
avoids committing an opaque binary model.
"""

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, Iterable, List, Optional

from utils.data_loader import get_products_for_country


TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass
class MappingResult:
    """A classifier result and the evidence record used to explain it."""

    product: Optional[dict]
    us_equivalent: Optional[str]
    confidence: float
    method: str
    alternatives: List[dict]


@dataclass
class DestinationMatch:
    """The reviewed destination product selected for an origin product."""

    product: Optional[dict]
    category: str
    direct_category: bool


CATEGORY_SUMMARIES = {
    "savings": "Both products are designed to keep personal savings accessible without a fixed maturity.",
    "transactions": "Both products are designed for receiving money and making routine payments or transfers.",
    "fixed_term": "Both products commit a lump sum for a stated term and use maturity-based conditions.",
    "recurring_savings": "Both products build a savings goal through repeated or automated contributions.",
    "basic_account": "Both products emphasize affordable access to essential deposit and payment services.",
}


def product_category(product: dict) -> str:
    """Return a country-neutral category used for destination matching."""
    equivalent = product.get("closest_us_equivalent", "").lower()
    product_id = product.get("id", "")
    if product_id == "us_savings" or equivalent == "savings account":
        return "savings"
    if product_id in {"us_checking", "us_interest_checking"} or "checking account" in equivalent:
        return "transactions"
    if product_id == "us_cd" or "certificate of deposit" in equivalent:
        return "fixed_term"
    if product_id == "us_goal_savings" or "goal-based recurring savings" in equivalent:
        return "recurring_savings"
    if product_id == "us_basic_account" or "low-cost basic bank account" in equivalent:
        return "basic_account"
    raise ValueError(f"Product {product_id!r} has no recognized mapping category")


def category_summary(category: str) -> str:
    return CATEGORY_SUMMARIES[category]


def find_destination_product(
    products: List[dict], origin_product: dict, destination_country: str
) -> DestinationMatch:
    """Choose the closest reviewed product in a destination country."""
    category = product_category(origin_product)
    destination_products = get_products_for_country(products, destination_country)
    direct_candidates = [
        product for product in destination_products if product_category(product) == category
    ]
    candidates = direct_candidates
    fallback_categories = {
        "basic_account": "transactions",
        "recurring_savings": "savings",
    }
    fallback_category = fallback_categories.get(category)
    if not candidates and fallback_category:
        candidates = [
            product
            for product in destination_products
            if product_category(product) == fallback_category
        ]
    if not candidates:
        return DestinationMatch(None, category, False)

    origin_words = set(
        _words(
            " ".join(
                [origin_product.get("description", "")]
                + origin_product.get("key_features", [])
            )
        )
    )

    def mechanics_score(product: dict) -> float:
        destination_words = set(
            _words(
                " ".join([product.get("description", "")] + product.get("key_features", []))
            )
        )
        union = origin_words | destination_words
        return len(origin_words & destination_words) / len(union) if union else 0.0

    selected = max(candidates, key=mechanics_score)
    return DestinationMatch(selected, category, bool(direct_candidates))


def _words(text: str) -> List[str]:
    words = TOKEN_RE.findall(text.lower())
    # A compact normalization is enough for product-language plurals without
    # adding a heavyweight NLP dependency to the Streamlit deployment.
    normalized = []
    for word in words:
        if len(word) > 4 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        normalized.append(word)
    return normalized


def _tokens(text: str) -> List[str]:
    words = _words(text)
    features = list(words)
    features.extend("word_pair=" + "_".join(pair) for pair in zip(words, words[1:]))
    return features


def _training_documents(product: dict) -> Iterable[str]:
    names = [product["product_name_local"]] + product.get("local_terms", [])
    details = [product.get("description", "")] + product.get("key_features", [])
    # Separate name documents make short user queries meaningful; the combined
    # document teaches the model product mechanics such as fixed term/check use.
    for name in names:
        yield name
        yield name + " " + " ".join(details)
    for detail in details:
        yield detail


class ProductMappingClassifier:
    """Multinomial Naive Bayes classifier implemented with the standard library."""

    def __init__(self, products: List[dict]):
        if not products:
            raise ValueError("At least one product is required to train the classifier")

        self.products = products
        self.class_document_counts = Counter()
        self.class_feature_counts = defaultdict(Counter)
        self.class_feature_totals = Counter()
        self.vocabulary = set()

        for product in products:
            label = product["closest_us_equivalent"]
            for document in _training_documents(product):
                features = _tokens(document)
                if not features:
                    continue
                self.class_document_counts[label] += 1
                counts = Counter(features)
                self.class_feature_counts[label].update(counts)
                self.class_feature_totals[label] += sum(counts.values())
                self.vocabulary.update(counts)

        self.labels = sorted(self.class_document_counts)
        self.document_total = sum(self.class_document_counts.values())

    def probabilities(self, text: str) -> Dict[str, float]:
        features = Counter(_tokens(text))
        if not features:
            return {}

        vocabulary_size = max(len(self.vocabulary), 1)
        log_scores = {}
        for label in self.labels:
            prior = self.class_document_counts[label] / self.document_total
            score = math.log(prior)
            denominator = self.class_feature_totals[label] + vocabulary_size
            counts = self.class_feature_counts[label]
            for feature, frequency in features.items():
                score += frequency * math.log((counts[feature] + 1) / denominator)
            log_scores[label] = score

        largest = max(log_scores.values())
        weights = {label: math.exp(score - largest) for label, score in log_scores.items()}
        total = sum(weights.values())
        return {label: weight / total for label, weight in weights.items()}


def _name_similarity(query: str, product: dict) -> float:
    query_normalized = " ".join(_words(query))
    names = [product["product_name_local"]] + product.get("local_terms", [])
    return max(
        SequenceMatcher(None, query_normalized, " ".join(_words(name))).ratio()
        for name in names
    )


def classify_product(
    products: List[dict],
    country: str,
    query: str,
    minimum_confidence: float = 0.42,
    classifier: Optional[ProductMappingClassifier] = None,
) -> MappingResult:
    """Map free text to a canonical category and its best reviewed origin record."""
    country_products = get_products_for_country(products, country)
    normalized_query = " ".join(_words(query))
    if not country_products or not normalized_query:
        return MappingResult(None, None, 0.0, "no_match", [])

    ranked_names = sorted(
        ((_name_similarity(query, product), product) for product in country_products),
        key=lambda item: item[0],
        reverse=True,
    )
    exact_product = next(
        (
            product
            for _, product in ranked_names
            if normalized_query
            in {" ".join(_words(name)) for name in [product["product_name_local"]] + product.get("local_terms", [])}
        ),
        None,
    )
    if exact_product:
        return MappingResult(
            exact_product,
            exact_product["closest_us_equivalent"],
            1.0,
            "exact",
            [product for _, product in ranked_names[1:3]],
        )

    classifier = classifier or ProductMappingClassifier(country_products)
    probabilities = classifier.probabilities(query)
    if not probabilities:
        return MappingResult(None, None, 0.0, "no_match", [])

    ranked_labels = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
    label, probability = ranked_labels[0]
    matching_products = [
        item for item in ranked_names if item[1]["closest_us_equivalent"] == label
    ]
    best_product = matching_products[0][1] if matching_products else ranked_names[0][1]

    # Blend model probability and surface-name similarity. This is displayed as
    # a routing confidence, not a statistical guarantee of financial equivalence.
    name_score = matching_products[0][0] if matching_products else 0.0
    confidence = (0.75 * probability) + (0.25 * name_score)
    alternatives = [product for _, product in ranked_names if product["id"] != best_product["id"]][:2]
    if confidence < minimum_confidence:
        return MappingResult(None, label, confidence, "low_confidence", alternatives)
    return MappingResult(best_product, label, confidence, "model", alternatives)
