from __future__ import annotations

import os
from typing import Any

import httpx
from typing import Optional
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleRequest

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_PROJECT_ID = os.getenv("GOOGLE_API_PROJECT_ID")
GOOGLE_API_MODEL = os.getenv("GOOGLE_API_MODEL", "gemini-1.5-pro")
GOOGLE_API_TIMEOUT = 30.0
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
FALLBACK_RANDOM_RESPONSES = os.getenv("FALLBACK_RANDOM_RESPONSES", "false").lower() in ("1", "true", "yes")


def _extract_text_from_response(response: dict[str, Any]) -> str:
    # Try several known response shapes from Generative Language API
    if not isinstance(response, dict):
        return str(response or "").strip()

    # candidates -> output|string or content
    candidates = response.get("candidates") or []
    if isinstance(candidates, list) and candidates:
        first = candidates[0]
        # direct text fields
        for key in ("output", "text", "content"):
            if key in first:
                val = first[key]
                if isinstance(val, str):
                    return val.strip()
                if isinstance(val, dict):
                    # nested content list
                    content = val.get("content")
                    if isinstance(content, str):
                        return content.strip()
                    if isinstance(content, list):
                        return "".join(
                            (piece.get("text", "") for piece in content if isinstance(piece, dict))
                        ).strip()

    # some responses include 'outputText' or 'text'
    for fallback in ("outputText", "text", "result", "content"):
        v = response.get(fallback)
        if isinstance(v, str) and v.strip():
            return v.strip()

    # nested candidates under 'result' or 'output'
    if "result" in response and isinstance(response["result"], dict):
        return _extract_text_from_response(response["result"]) or ""

    return "" if response is None else str(response)


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
    # Try a short model path first, then fall back to a project-scoped path
    # Build auth: prefer service account bearer token if provided, otherwise use API key param
    headers: dict[str, str] = {}
    params: dict[str, str] | None = None

    if GOOGLE_SERVICE_ACCOUNT_FILE and os.path.exists(GOOGLE_SERVICE_ACCOUNT_FILE):
        try:
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            creds.refresh(GoogleRequest())
            token = creds.token
            headers = {"Authorization": f"Bearer {token}"}
        except Exception as exc:
            return f"Failed to load service account credentials: {exc}"
    else:
        if GOOGLE_API_KEY:
            params = {"key": GOOGLE_API_KEY}
        else:
            return (
                "Google AI Studio is not configured. "
                "Set GOOGLE_API_KEY or GOOGLE_SERVICE_ACCOUNT_FILE in your environment and restart the app."
            )

    payload = {
        "prompt": {"text": prompt},
        "temperature": temperature,
        "maxOutputTokens": max_output_tokens,
    }

    def _post(endpoint_url: str):
        resp = httpx.post(endpoint_url, params=params, headers=headers or None, json=payload, timeout=GOOGLE_API_TIMEOUT)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            # Re-raise so callers can inspect status_code/text
            raise
        return resp

    # first attempt: public model path
    short_endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta2/models/{model}:generateText"
    )

    try:
        response = _post(short_endpoint)
        return _extract_text_from_response(response.json())
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        text = exc.response.text

        # If model not found (404) and we have a project id, try project-scoped endpoint
        if status == 404 and GOOGLE_API_PROJECT_ID:
            proj_endpoint = (
                f"https://generativelanguage.googleapis.com/v1beta2/projects/{GOOGLE_API_PROJECT_ID}/locations/us-central1/models/{model}:generateText"
            )
            try:
                response = _post(proj_endpoint)
                return _extract_text_from_response(response.json())
            except httpx.HTTPStatusError as exc2:
                # if the requested Gemini model isn't available, try a fallback model
                fallback_models = ["text-bison-001"]
                for fb in fallback_models:
                    try:
                        fb_short = f"https://generativelanguage.googleapis.com/v1beta2/models/{fb}:generateText"
                        resp_fb = _post(fb_short)
                        return _extract_text_from_response(resp_fb.json())
                    except httpx.HTTPStatusError:
                        # try project-scoped fallback
                        if GOOGLE_API_PROJECT_ID:
                            fb_proj = (
                                f"https://generativelanguage.googleapis.com/v1beta2/projects/{GOOGLE_API_PROJECT_ID}/locations/us-central1/models/{fb}:generateText"
                            )
                            try:
                                resp_fb2 = _post(fb_proj)
                                return _extract_text_from_response(resp_fb2.json())
                            except httpx.HTTPStatusError:
                                continue

                return f"Google AI Studio request failed (project endpoint): {exc2.response.status_code} {exc2.response.text}"
        # if not a 404 or fallbacks didn't help, return original error
        # If configured, return a local randomized fallback instead of the raw error
        if FALLBACK_RANDOM_RESPONSES:
            return _local_random_response(prompt)

        return f"Google AI Studio request failed: {status} {text}"
    except Exception as exc:
        if FALLBACK_RANDOM_RESPONSES:
            return _local_random_response(prompt)
        return f"Google AI Studio request error: {exc}"


def check_google_configuration(model_id: str | None = None) -> dict[str, object]:
    """Return diagnostic info for the configured API key, project and model endpoints.

    This attempts the short model endpoint and, if available, a project-scoped endpoint
    and returns the HTTP status and response text for each attempt. Useful for debugging
    404/NOT_FOUND issues when a model or project isn't accessible.
    """
    model = model_id or GOOGLE_API_MODEL
    auth_info: dict[str, object] = {}
    params = None
    headers: dict[str, str] | None = None

    if GOOGLE_SERVICE_ACCOUNT_FILE and os.path.exists(GOOGLE_SERVICE_ACCOUNT_FILE):
        auth_info["auth_method"] = "service_account"
        try:
            creds = service_account.Credentials.from_service_account_file(
                GOOGLE_SERVICE_ACCOUNT_FILE,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            creds.refresh(GoogleRequest())
            headers = {"Authorization": f"Bearer {creds.token}"}
        except Exception as exc:
            auth_info["error"] = str(exc)
    elif GOOGLE_API_KEY:
        auth_info["auth_method"] = "api_key"
        params = {"key": GOOGLE_API_KEY}
    else:
        auth_info["auth_method"] = "none"

    payload = {"prompt": {"text": "diagnostic"}, "maxOutputTokens": 2}

    attempts: list[dict[str, object]] = []

    short_endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta2/models/{model}:generateText"
    )
    try:
        resp = httpx.post(short_endpoint, params=params, headers=headers or None, json=payload, timeout=GOOGLE_API_TIMEOUT)
        attempts.append({"endpoint": short_endpoint, "status": resp.status_code, "text": resp.text})
    except Exception as exc:
        attempts.append({"endpoint": short_endpoint, "error": str(exc)})

    if GOOGLE_API_PROJECT_ID:
        proj_endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta2/projects/{GOOGLE_API_PROJECT_ID}/locations/us-central1/models/{model}:generateText"
        )
        try:
            resp = httpx.post(proj_endpoint, params=params, headers=headers or None, json=payload, timeout=GOOGLE_API_TIMEOUT)
            attempts.append({"endpoint": proj_endpoint, "status": resp.status_code, "text": resp.text})
        except Exception as exc:
            attempts.append({"endpoint": proj_endpoint, "error": str(exc)})

    out = {
        "auth": auth_info,
        "project_id": GOOGLE_API_PROJECT_ID,
        "model": model,
        "attempts": attempts,
    }
    return out


def _local_random_response(prompt: str) -> str:
    """Return a short randomized fallback answer for development/testing."""
    import random

    samples = [
        "Here's a concise explanation: it's about patterns and data.",
        "In short: it's a system that learns from examples and makes predictions.",
        "Think of it as code that improves by finding patterns in information.",
        "A simple answer: models map inputs to outputs using learned weights.",
        "It's like teaching a student by showing many examples until they generalize."
    ]

    # echo minimal transformation of prompt to appear context-aware
    short = prompt.strip()[:120]
    return f"{random.choice(samples)} (prompt preview: '{short}')"
