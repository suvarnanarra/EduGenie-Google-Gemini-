from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

from edugenie.explanation_module import explain_concept
from edugenie.learning_path import build_learning_recommendations
from edugenie.qna import answer_question
from edugenie.quiz_module import generate_quiz
from edugenie.summary_module import summarize_text

app = FastAPI(title="EduGenie Learning Assistant")


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return Path("templates/index.html").read_text(encoding="utf-8")


@app.post("/ask")
def ask(question: str) -> dict[str, str]:
    return {"answer": answer_question(question)}


@app.post("/explain")
def explain(concept: str) -> dict[str, str]:
    return {"explanation": explain_concept(concept)}


@app.post("/quiz")
def quiz(topic: str) -> dict[str, str]:
    return {"quiz": generate_quiz(topic)}


@app.post("/summarize")
def summarize(text: str) -> dict[str, str]:
    return {"summary": summarize_text(text)}


@app.post("/recommend")
def recommend(topic: str) -> dict[str, str]:
    return {"recommendations": build_learning_recommendations(topic)}
