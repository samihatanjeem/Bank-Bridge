import json
import unittest

from utils.data_loader import load_account_opening_process, load_financial_products
from utils.passport import (
    PASSPORT_SCHEMA,
    analyze_document,
    build_access_plan,
    demo_extraction,
    document_content,
    goal_options,
    passport_markdown,
)


class FakeResponses:
    def __init__(self, result):
        self.result = result
        self.request = None

    def create(self, **kwargs):
        self.request = kwargs
        return type(
            "FakeResponse",
            (),
            {"status": "completed", "output_text": json.dumps(self.result)},
        )()


class FakeClient:
    def __init__(self, result):
        self.responses = FakeResponses(result)


class PassportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.products = load_financial_products()
        cls.processes = load_account_opening_process()

    def test_demo_matches_strict_schema_shape(self):
        result = demo_extraction("India")
        self.assertEqual(set(result), set(PASSPORT_SCHEMA["required"]))
        self.assertNotIn("DEMO USER", json.dumps(result))
        self.assertNotIn("4821", json.dumps(result))

    def test_image_and_pdf_content_are_direct_data_inputs(self):
        image = document_content(b"image", "statement.png", "image/png")
        pdf = document_content(b"pdf", "statement.pdf", "application/pdf")
        text = document_content(b"text", "statement.txt", "text/plain")
        self.assertEqual(image["type"], "input_image")
        self.assertTrue(image["image_url"].startswith("data:image/png;base64,"))
        self.assertEqual(pdf["type"], "input_file")
        self.assertEqual(pdf["detail"], "high")
        self.assertNotIn("detail", text)

    def test_openai_request_is_structured_and_not_stored(self):
        expected = demo_extraction("India")
        client = FakeClient(expected)
        result = analyze_document(
            b"fictional statement",
            "demo.txt",
            "text/plain",
            "India",
            client=client,
        )
        request = client.responses.request
        self.assertEqual(result, expected)
        self.assertFalse(request["store"])
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertEqual(request["text"]["format"]["schema"], PASSPORT_SCHEMA)

    def test_every_goal_builds_a_sourced_us_plan(self):
        extraction = demo_extraction("India")
        for goal in goal_options():
            with self.subTest(goal=goal):
                plan = build_access_plan(
                    extraction,
                    "India",
                    "United States",
                    goal,
                    self.products,
                    self.processes,
                )
                self.assertEqual(len(plan["steps"]), 4)
                self.assertTrue(plan["requirements"])
                self.assertTrue(plan["sources"])
                self.assertEqual(plan["readiness_complete"], 4)

    def test_download_excludes_direct_identifiers(self):
        extraction = demo_extraction("India")
        plan = build_access_plan(
            extraction,
            "India",
            "United States",
            "Open my first account",
            self.products,
            self.processes,
        )
        artifact = passport_markdown(extraction, plan)
        self.assertIn("not a credit score", artifact)
        self.assertNotIn("DEMO USER", artifact)
        self.assertNotIn("4821", artifact)


if __name__ == "__main__":
    unittest.main()
