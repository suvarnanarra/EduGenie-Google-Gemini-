from __future__ import annotations

from .router import ModelRouter

router = ModelRouter()


def summarize_text(text: str, prefer_fast: bool = False) -> str:
    prompt = (
        "You are an educational summarizer. Create a clear, concise summary while preserving the main ideas. "
        "Keep it easy to understand and avoid unnecessary repetition.\n\n"
        f"Text to summarize:\n{text}"
    )
    adapter = router.select_model("summarization", prefer_fast=prefer_fast)
    response = adapter.generate(prompt)
    return response.strip() or "I could not generate a summary for that text right now."
