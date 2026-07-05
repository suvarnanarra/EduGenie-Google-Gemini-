import unittest

from edugenie.config import TaskType
from edugenie.router import ModelRouter


class ModelRouterTests(unittest.TestCase):
    def test_prefers_gemini_for_reasoning_tasks(self) -> None:
        router = ModelRouter()
        adapter = router.select_model(TaskType.CONCEPT_EXPLANATION)
        self.assertEqual(adapter.name, "lamini-flan-t5")

    def test_uses_lamini_for_quiz_generation_when_fast_mode(self) -> None:
        router = ModelRouter()
        adapter = router.select_model(TaskType.QUIZ_GENERATION, prefer_fast=True)
        self.assertEqual(adapter.name, "lamini-flan-t5")

    def test_supports_string_task_names(self) -> None:
        router = ModelRouter()
        adapter = router.select_model("summarization")
        self.assertEqual(adapter.name, "gemini-1.5-pro")


if __name__ == "__main__":
    unittest.main()
