from enum import Enum


class TaskType(str, Enum):
    QUESTION_ANSWERING = "question_answering"
    SUMMARIZATION = "summarization"
    QUIZ_GENERATION = "quiz_generation"
    LEARNING_RECOMMENDATIONS = "learning_recommendations"
    CONCEPT_EXPLANATION = "concept_explanation"
