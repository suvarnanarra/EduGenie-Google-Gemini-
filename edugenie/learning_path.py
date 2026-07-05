from __future__ import annotations

import random

from .router import ModelRouter

router = ModelRouter()


def build_learning_recommendations(topic: str, level: str = "beginner", prefer_fast: bool = False) -> str:
    clean_topic = " ".join(topic.strip().split()) or "this topic"
    intro = random.choice(
        [
            f"Here is a simple learning plan for {clean_topic}:",
            f"Start learning {clean_topic} with this beginner-friendly path:",
            f"Use this study plan to build confidence in {clean_topic}:",
        ]
    )
    return (
        f"{intro}\n\n"
        f"1. Basics: Learn the definition and key terms of {clean_topic}.\n"
        f"2. Examples: Study two simple examples and write short notes.\n"
        f"3. Practice: Solve small questions daily for 15-20 minutes.\n"
        f"4. Revision: Make flashcards or a one-page summary.\n"
        f"5. Next step: Try a mini project or quiz to check your understanding."
    )
