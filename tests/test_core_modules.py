import unittest
from unittest.mock import patch

from edugenie.quiz_module import generate_quiz


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


if __name__ == "__main__":
    unittest.main()
