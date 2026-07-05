from __future__ import annotations

from typing import Any

from __future__ import annotations

from typing import Any

from .config import TaskType
from .google_adapter import get_google_response


class BaseModelAdapter:
    def __init__(self, name: str, model_id: str) -> None:
        self.name = name
        self.model_id = model_id

    def generate(self, prompt: str, **_: Any) -> str:
        return get_google_response(prompt, model_id=self.model_id)


class GeminiAdapter(BaseModelAdapter):
    def __init__(self) -> None:
        super().__init__("gemini-1.5-pro", "gemini-1.5-pro")


class LaMiniAdapter(BaseModelAdapter):
    def __init__(self) -> None:
        super().__init__("lamini-flan-t5", "lamini/flan-t5")


class ModelRouter:
    def __init__(self) -> None:
        self.gemini = GeminiAdapter()
        self.lamini = LaMiniAdapter()

    def select_model(self, task: TaskType | str, prefer_fast: bool = False) -> BaseModelAdapter:
        if isinstance(task, str):
            task = TaskType(task)

        if task in {
            TaskType.CONCEPT_EXPLANATION,
            TaskType.LEARNING_RECOMMENDATIONS,
            TaskType.QUESTION_ANSWERING,
            TaskType.SUMMARIZATION,
        }:
            return self.gemini

        if task == TaskType.QUIZ_GENERATION and prefer_fast:
            return self.lamini

        return self.gemini
