from __future__ import annotations

from typing import Optional

from .router import ModelRouter

router = ModelRouter()


def answer_question(question: str, context: Optional[str] = None, prefer_fast: bool = False) -> str:
    prompt = (
        "You are a helpful educational assistant. Answer the question accurately, clearly, and concisely. "
        "If the question is ambiguous, mention the most likely interpretation.\n\n"
        f"Question: {question}"
    )
    if context:
        prompt += f"\nContext: {context}"

    adapter = router.select_model("question_answering", prefer_fast=prefer_fast)
    response = adapter.generate(prompt)
    return response.strip() or "I could not generate an answer for that question right now."
