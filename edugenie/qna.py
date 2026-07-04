from __future__ import annotations

from typing import Optional

from .router import ModelRouter

router = ModelRouter()


def answer_question(question: str, context: Optional[str] = None, prefer_fast: bool = False) -> str:
    prompt = f"Answer the following question clearly and concisely:\nQuestion: {question}"
    if context:
        prompt += f"\nContext: {context}"

    adapter = router.select_model("question_answering", prefer_fast=prefer_fast)
    return adapter.generate(prompt)
