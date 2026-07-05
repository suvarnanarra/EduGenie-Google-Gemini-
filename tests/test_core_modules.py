import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from edugenie.quiz_module import generate_quiz
from main import app


class QuizModuleTests(unittest.TestCase):
    def test_generate_quiz_parses_markdown_json_into_python_objects(self) -> None:
        class FakeAdapter:
            def generate(self, prompt: str) -> str:
                return '''```json
[ 
  {
    "question": "What is photosynthesis?",
    "options": ["A process plants use to make food", "A type of soil", "A weather event", "A kind of animal"],
    "correct_answer": "A process plants use to make food"
  }
]
```'''

        with patch("edugenie.quiz_module.router.select_model", return_value=FakeAdapter()):
            result = generate_quiz("Photosynthesis", question_count=1)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["question"], "What is photosynthesis?")
        self.assertEqual(result[0]["correct_answer"], "A process plants use to make food")

    def test_generate_quiz_returns_empty_list_when_response_is_invalid(self) -> None:
        class FakeAdapter:
            def generate(self, prompt: str) -> str:
                return "This is not valid JSON"

        with patch("edugenie.quiz_module.router.select_model", return_value=FakeAdapter()):
            result = generate_quiz("Photosynthesis", question_count=1)

        self.assertEqual(result, [])


class AppRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_homepage_serves_ui(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("EduGenie Learning Assistant", response.text)

    def test_health_endpoint_is_available(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_core_feature_endpoints_return_expected_keys(self) -> None:
        endpoints = [
            ("/qa", {"question": "What is Python?"}),
            ("/explain", {"concept": "Python"}),
            ("/quiz", {"topic": "Python", "question_count": 2}),
            ("/summarize", {"text": "A short paragraph to summarize."}),
            ("/learn/recommendations", {"topic": "Python", "level": "beginner"}),
        ]

        for path, payload in endpoints:
            response = self.client.post(path, json=payload)
            self.assertEqual(response.status_code, 200, msg=path)
            self.assertTrue(response.json())


if __name__ == "__main__":
    unittest.main()
