from __future__ import annotations

from .router import ModelRouter

router = ModelRouter()


def summarize_text(text: str, prefer_fast: bool = False) -> str:
    prompt = f"Summarize the following text in a clear and concise way:\n{text}"
    adapter = router.select_model("summarization", prefer_fast=prefer_fast)
    return adapter.generate(prompt)
