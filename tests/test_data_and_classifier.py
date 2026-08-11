import json
import unittest
from pathlib import Path

from utils.data_loader import (
    find_product_by_term,
    get_process_for_country,
    load_account_opening_process,
    load_financial_products,
)
from utils.product_classifier import classify_product


ROOT = Path(__file__).parent.parent
SUPPORTED_COUNTRIES = {
    "Bangladesh",
    "China",
    "Dominican Republic",
    "El Salvador",
    "India",
    "Mexico",
    "Philippines",
    "South Korea",
    "United Kingdom",
    "Vietnam",
}


class DatasetTests(unittest.TestCase):
    def test_json_files_are_valid(self):
        for filename in [
            "financial_products.json",
            "additional_financial_products.json",
            "account_opening_process.json",
            "additional_account_opening_process.json",
        ]:
            with open(ROOT / "data" / filename, encoding="utf-8") as data_file:
                self.assertIsInstance(json.load(data_file), list)

    def test_every_supported_country_has_products_process_and_sources(self):
        products = load_financial_products()
        processes = load_account_opening_process()
        product_countries = {product["country"] for product in products} - {"United States"}
        process_countries = {process["country"] for process in processes} - {"United States"}
        self.assertEqual(product_countries, SUPPORTED_COUNTRIES)
        self.assertEqual(process_countries, SUPPORTED_COUNTRIES)
        for country in SUPPORTED_COUNTRIES:
            records = [product for product in products if product["country"] == country]
            self.assertGreaterEqual(len(records), 4)
            self.assertTrue(all(product.get("sources") for product in records))
            process = get_process_for_country(processes, country)
            self.assertTrue(process.get("sources"))

    def test_optional_lookups_work_on_python_39(self):
        products = load_financial_products()
        processes = load_account_opening_process()
        self.assertEqual(find_product_by_term(products, "Bangladesh", "FDR")["id"], "bd_fdr")
        self.assertIsNone(find_product_by_term(products, "Bangladesh", "unknown"))
        self.assertEqual(get_process_for_country(processes, "India")["country"], "India")


class ClassifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.products = load_financial_products()

    def assert_mapping(self, country, query, expected_equivalent):
        result = classify_product(self.products, country, query)
        self.assertIsNotNone(result.product)
        self.assertEqual(result.us_equivalent, expected_equivalent)

    def test_exact_abbreviation(self):
        self.assert_mapping("Bangladesh", "DPS", "Goal-based recurring savings (no direct standard US equivalent)")

    def test_description_to_cd(self):
        self.assert_mapping("Philippines", "deposit until a fixed maturity", "Certificate of Deposit (CD)")

    def test_description_to_checking(self):
        self.assert_mapping("Philippines", "write checks for bills", "Checking account")

    def test_unknown_text_is_not_presented_as_a_match(self):
        result = classify_product(self.products, "India", "gibberish quux")
        self.assertIsNone(result.product)
        self.assertEqual(result.method, "low_confidence")

    def test_new_country_mappings(self):
        cases = [
            ("China", "fixed lump sum until maturity", "Certificate of Deposit (CD)"),
            ("Mexico", "Pagaré", "Certificate of Deposit (CD)"),
            ("Vietnam", "account for bills and card payments", "Checking account"),
            ("South Korea", "monthly installment savings", "Goal-based recurring savings (no direct standard US equivalent)"),
            ("El Salvador", "Cuenta Corriente", "Checking account"),
            ("Dominican Republic", "Certificado Financiero", "Certificate of Deposit (CD)"),
            ("United Kingdom", "Regular Saver", "Goal-based recurring savings (no direct standard US equivalent)"),
        ]
        for country, query, equivalent in cases:
            with self.subTest(country=country):
                self.assert_mapping(country, query, equivalent)

    def test_cached_classifier_can_be_reused(self):
        from utils.data_loader import get_products_for_country
        from utils.product_classifier import ProductMappingClassifier

        classifier = ProductMappingClassifier(get_products_for_country(self.products, "India"))
        result = classify_product(
            self.products,
            "India",
            "fixed monthly installment savings",
            classifier=classifier,
        )
        self.assertEqual(
            result.us_equivalent,
            "Goal-based recurring savings (no direct standard US equivalent)",
        )


if __name__ == "__main__":
    unittest.main()
