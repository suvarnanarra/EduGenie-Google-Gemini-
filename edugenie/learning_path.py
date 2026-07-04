from __future__ import annotations

from .router import ModelRouter

router = ModelRouter()


def build_learning_recommendations(topic: str, level: str = "beginner", prefer_fast: bool = False) -> str:
    prompt = f"Recommend a learning path for '{topic}' for a {level} learner."
    adapter = router.select_model("learning_recommendations", prefer_fast=prefer_fast)
    return adapter.generate(prompt)
