"""Local Ollama API client helpers."""

from __future__ import annotations

import json
import urllib.request

from proof_please.pipeline.models import OllamaConfig


def _endpoint(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}{path}"


def list_ollama_models(config: OllamaConfig) -> list[str]:
    """Fetch installed model names from Ollama /api/tags."""
    req = urllib.request.Request(
        _endpoint(config.base_url, "/api/tags"),
        headers={"Content-Type": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=config.timeout) as resp:
        data = json.load(resp)
    models = data.get("models", [])
    names: list[str] = []
    for model in models:
        name = model.get("name") or model.get("model")
        if isinstance(name, str) and name:
            names.append(name)
    return names


def ollama_chat(config: OllamaConfig, model: str, messages: list[dict[str, str]]) -> str:
    """Call Ollama /api/chat and return message content."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {
            "temperature": 0.0,
            "num_predict": 1200,
        },
    }
    req = urllib.request.Request(
        _endpoint(config.base_url, "/api/chat"),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=config.timeout) as resp:
        body = json.load(resp)
    message = body.get("message", {})
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("Ollama response missing message content.")
    return content
