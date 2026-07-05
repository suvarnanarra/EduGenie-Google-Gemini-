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

    def generate(self, prompt: str, **_: Any) -> str:
        # Try local transformers-based LaMini if available, otherwise fall back to cloud
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            import torch

            model_name = "MBZUAI/LaMini-Flan-T5-783M"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            inputs = tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=150, do_sample=False)
            text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return text.strip()
        except Exception:
            # fallback to cloud API via BaseModelAdapter
            return super().generate(prompt, **_)


class ModelRouter:
    def __init__(self) -> None:
        self.gemini = GeminiAdapter()
        self.lamini = LaMiniAdapter()

    def select_model(self, task: TaskType | str, prefer_fast: bool = False) -> BaseModelAdapter:
        if isinstance(task, str):
            task = TaskType(task)

        # Use LaMini for concept explanations if available (local first),
        # use Gemini for Q/A, summarization, and recommendations.
        if task == TaskType.CONCEPT_EXPLANATION:
            return self.lamini

        if task in {
            TaskType.LEARNING_RECOMMENDATIONS,
            TaskType.QUESTION_ANSWERING,
            TaskType.SUMMARIZATION,
        }:
            return self.gemini

        if task == TaskType.QUIZ_GENERATION and prefer_fast:
            return self.lamini

        return self.gemini
