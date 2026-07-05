import unittest

from fastapi.testclient import TestClient

from edugenie.quiz_module import generate_quiz
from main import app


class QuizModuleTests(unittest.TestCase):
    def test_generate_quiz_returns_python_objects(self) -> None:
        result = generate_quiz("Photosynthesis", question_count=2)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn("question", result[0])
        self.assertIn("options", result[0])
        self.assertIn("correct_answer", result[0])
        self.assertIsInstance(result[0]["options"], list)

    def test_generate_quiz_limits_question_count(self) -> None:
        result = generate_quiz("Photosynthesis", question_count=20)

        self.assertEqual(len(result), 5)


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
