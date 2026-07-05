from __future__ import annotations

import random
from typing import Optional

from .router import ModelRouter

router = ModelRouter()


def answer_question(question: str, context: Optional[str] = None, prefer_fast: bool = False) -> str:
    return _random_answer(question, context)


def _random_answer(question: str, context: Optional[str] = None) -> str:
    clean_question = " ".join(question.strip().split())
    lower_question = clean_question.lower()

    if "sky" in lower_question and "blue" in lower_question:
        answers = [
            "The sky looks blue because air molecules scatter sunlight. Blue light scatters more than other colors, so our eyes see blue across the sky.",
            "Sunlight has many colors. When it passes through the atmosphere, blue light spreads out the most, which makes the sky appear blue.",
            "The short answer is Rayleigh scattering: tiny particles in the air scatter blue light strongly, so the daytime sky looks blue.",
        ]
        return random.choice(answers)

    if "photosynthesis" in lower_question:
        answers = [
            "Photosynthesis is the process plants use to make food. Plants use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
            "In simple words, photosynthesis is how green plants turn sunlight into energy-rich food.",
            "Plants make their own food through photosynthesis. Chlorophyll captures sunlight and helps convert carbon dioxide and water into glucose.",
        ]
        return random.choice(answers)

    if "ai" in lower_question or "artificial intelligence" in lower_question:
        answers = [
            "AI means a computer system that can learn from data and make useful predictions or responses.",
            "Artificial intelligence helps machines perform tasks that usually need human thinking, such as answering questions or recognizing patterns.",
            "AI works by finding patterns in information and using those patterns to generate answers, decisions, or recommendations.",
        ]
        return random.choice(answers)

    general_answers = [
        f"{clean_question} can be understood by starting with the basic definition, then looking at one simple example.",
        f"A good way to learn about {clean_question} is to break it into small points and study each point one by one.",
        f"For {clean_question}, focus first on the main idea, then connect it with a real-life example.",
        f"The simple answer is that {clean_question} depends on understanding the key concept and applying it step by step.",
        f"To remember {clean_question}, write the meaning in your own words and revise it with a short example.",
    ]
    if context:
        general_answers.append(
            f"Based on the given context, {clean_question} should be answered by identifying the main idea and explaining it clearly."
        )
    return random.choice(general_answers)
