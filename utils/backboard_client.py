import os
from typing import Any

import requests


class BackboardMemoryClient:
    """Uses Backboard only for Memory Lite storage/retrieval, never response generation."""

    BASE_URL = "https://app.backboard.io/api"

    def __init__(self) -> None:
        self.api_key = os.getenv("BACKBOARD_API_KEY", "")
        self.default_assistant_id = os.getenv("BACKBOARD_ASSISTANT_ID", "")

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise RuntimeError("BACKBOARD_API_KEY is not configured.")
        return {"X-API-Key": self.api_key, "Content-Type": "application/json"}

    def retrieve_context(self, assistant_id: str | None) -> str:
        """Read extracted Memory Lite facts directly; this does not invoke Backboard's LLM."""
        assistant_id = assistant_id or self.default_assistant_id
        if not assistant_id:
            return ""
        try:
            response = requests.get(
                f"{self.BASE_URL}/assistants/{assistant_id}/memories", headers=self._headers(),
                params={"page": 1, "page_size": 12}, timeout=30,
            )
            response.raise_for_status()
            memories = response.json().get("memories", [])
        except requests.RequestException as exc:
            raise RuntimeError(f"Backboard memory retrieval failed: {exc}") from exc
        facts = []
        for item in memories:
            if isinstance(item, str):
                facts.append(item)
            elif isinstance(item, dict):
                facts.append(str(item.get("content") or item.get("memory") or item.get("text") or ""))
        return "\n".join(f"- {fact}" for fact in facts if fact)[:5000]

    def save_interaction(self, query: str, answer: str, assistant_id: str | None) -> str | None:
        """Save with memory='Auto' but explicitly suppress Backboard LLM inference."""
        payload: dict[str, Any] = {
            "content": f"Learner question: {query}\nQuantCoach (Groq) answer: {answer}",
            "memory": "Auto", "send_to_llm": "false", "stream": False,
            "metadata": {"source": "quantcoach", "generator": "groq"},
        }
        resolved_id = assistant_id or self.default_assistant_id
        if resolved_id:
            payload["assistant_id"] = resolved_id
        try:
            response = requests.post(f"{self.BASE_URL}/threads/messages", headers=self._headers(), json=payload, timeout=45)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise RuntimeError(f"Backboard memory save failed: {exc}") from exc
        return data.get("assistant_id") or resolved_id
