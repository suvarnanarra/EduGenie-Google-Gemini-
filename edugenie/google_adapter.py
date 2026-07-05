from __future__ import annotations

import os
from typing import Any

import httpx

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_PROJECT_ID = os.getenv("GOOGLE_API_PROJECT_ID")
GOOGLE_API_MODEL = os.getenv("GOOGLE_API_MODEL", "gemini-1.5-pro")
GOOGLE_API_TIMEOUT = 30.0


def _extract_text_from_response(response: dict[str, Any]) -> str:
    candidates = response.get("candidates") or []
    if isinstance(candidates, list) and candidates:
        first = candidates[0]
        output = first.get("output")
        if isinstance(output, str):
            return output.strip()
        if isinstance(output, dict):
            content = output.get("content")
            if isinstance(content, str):
                return content.strip()
            if isinstance(content, list):
                return "".join(
                    piece.get("text", "")
                    for piece in content
                    if isinstance(piece, dict)
                ).strip()
    return str(response.get("text", "")).strip()


def get_google_response(
    prompt: str,
    model_id: str | None = None,
    temperature: float = 0.2,
    max_output_tokens: int = 512,
) -> str:
    if not GOOGLE_API_KEY:
        return (
            "Google AI Studio is not configured. "
            "Set GOOGLE_API_KEY in your environment and restart the app."
        )

    model = model_id or GOOGLE_API_MODEL
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta2/models/{model}:generateText"
    )
    params = {"key": GOOGLE_API_KEY}
    payload = {
        "prompt": {"text": prompt},
        "temperature": temperature,
        "maxOutputTokens": max_output_tokens,
    }

    try:
        response = httpx.post(endpoint, params=params, json=payload, timeout=GOOGLE_API_TIMEOUT)
        response.raise_for_status()
        return _extract_text_from_response(response.json())
    except httpx.HTTPStatusError as exc:
        return (
            f"Google AI Studio request failed: {exc.response.status_code} "
            f"{exc.response.text}"
        )
    except Exception as exc:
        return f"Google AI Studio request error: {exc}"
