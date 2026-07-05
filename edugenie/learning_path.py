from __future__ import annotations

from .router import ModelRouter

router = ModelRouter()


def build_learning_recommendations(topic: str, level: str = "beginner", prefer_fast: bool = False) -> str:
    prompt = (
        "You are an educational planner. Create a structured learning path for the topic from beginner to advanced. "
        "For each stage, mention the key concept, what the learner should practice, and good resources such as videos, articles, or books.\n\n"
        f"Topic: {topic}\n"
        f"Learner level: {level}"
    )
    adapter = router.select_model("learning_recommendations", prefer_fast=prefer_fast)
    response = adapter.generate(prompt)
    return response.strip() or "I could not generate a learning path for that topic right now."
