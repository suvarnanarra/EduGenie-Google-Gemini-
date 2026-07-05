from pathlib import Path
import os

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from edugenie.explanation_module import explain_concept
from edugenie.learning_path import build_learning_recommendations
from edugenie.qna import answer_question
from edugenie.quiz_module import generate_quiz
from edugenie.summary_module import summarize_text
from edugenie.google_adapter import check_google_configuration

app = FastAPI(title="EduGenie Learning Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")


class QARequest(BaseModel):
    question: str
    context: str | None = None


class ExplainRequest(BaseModel):
    concept: str
    detail: str | None = None


class QuizRequest(BaseModel):
    topic: str
    question_count: int = 5


class SummarizeRequest(BaseModel):
    text: str


class LearningRecommendationRequest(BaseModel):
    topic: str
    level: str = "beginner"


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return Path("templates/index.html").read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/key")
def health_key(model: str | None = None) -> dict[str, object]:
    """Diagnostic endpoint to check Google API key, project and model access."""
    return check_google_configuration(model)


@app.get("/qa")
def qa_get(question: str = Query(..., min_length=1), context: str | None = None) -> dict[str, str]:
    return {"answer": answer_question(question, context)}


@app.post("/qa")
def qa(payload: QARequest) -> dict[str, str]:
    return {"answer": answer_question(payload.question, payload.context)}


@app.post("/explain")
def explain(payload: ExplainRequest) -> dict[str, str]:
    return {"explanation": explain_concept(payload.concept, payload.detail or "")}


@app.post("/quiz")
def quiz(payload: QuizRequest) -> dict[str, object]:
    return {"quiz": generate_quiz(payload.topic, payload.question_count)}


@app.post("/summarize")
def summarize(payload: SummarizeRequest) -> dict[str, str]:
    return {"summary": summarize_text(payload.text)}


@app.post("/learn/recommendations")
def learn_recommendations(payload: LearningRecommendationRequest) -> dict[str, str]:
    return {"recommendations": build_learning_recommendations(payload.topic, payload.level)}


@app.get("/learn/recommendations")
def learn_recommendations_get(topic: str = Query(..., min_length=1), level: str = "beginner") -> dict[str, str]:
    return {"recommendations": build_learning_recommendations(topic, level)}


@app.post("/ask")
def ask(payload: QARequest) -> dict[str, str]:
    return qa(payload)


@app.post("/recommend")
def recommend(payload: LearningRecommendationRequest) -> dict[str, str]:
    return learn_recommendations(payload)
