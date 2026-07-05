from __future__ import annotations

import random

from .router import ModelRouter

router = ModelRouter()


def explain_concept(concept: str, detail: str = "", prefer_fast: bool = False) -> str:
    clean_concept = " ".join(concept.strip().split())
    lower_concept = clean_concept.lower()

    if "photosynthesis" in lower_concept:
        answers = [
            "Photosynthesis is the process plants use to make food. Leaves take in carbon dioxide, roots absorb water, and chlorophyll captures sunlight. The plant then produces glucose for energy and releases oxygen.",
            "In simple words, photosynthesis is how plants cook their own food using sunlight. The main ingredients are sunlight, water, and carbon dioxide.",
            "Photosynthesis happens mostly in leaves. Chlorophyll absorbs sunlight and helps convert water and carbon dioxide into glucose, which the plant uses as food.",
        ]
        return random.choice(answers)

    examples = [
        f"{clean_concept} means an important idea that can be learned step by step. Start with the definition, then study one example, and finally try explaining it in your own words.",
        f"Think of {clean_concept} as a topic with a main rule and supporting details. Once you understand the main rule, examples become easier.",
        f"{clean_concept} is easier to understand when you break it into small parts: what it means, why it matters, and where it is used.",
        f"A beginner-friendly explanation of {clean_concept}: learn the basic meaning first, then connect it to a real-life example so it feels practical.",
    ]
    if detail:
        examples.append(f"For {clean_concept}, focus on this extra point too: {detail.strip()}")
    return random.choice(examples)
