import os

import requests


class GroqClient:
    """Minimal OpenAI-compatible client used solely for response generation."""

    URL = "https://api.groq.com/openai/v1/chat/completions"
    RESPONSES_URL = "https://api.groq.com/openai/v1/responses"

    def __init__(self) -> None:
        self.api_key = os.getenv("GROQ_API_KEY", "")
        # Groq's OpenAI-compatible endpoint; response generation never goes through Backboard.
        self.model = os.getenv("GROQ_MODEL_NAME", "openai/gpt-oss-120b")

    def chat(self, messages: list[dict]) -> str:
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is not configured.")
        try:
            response = requests.post(
                self.URL,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": messages, "temperature": 0.3, "max_completion_tokens": 1200},
                timeout=90,
            )
            # Chat Completions is the primary, documented OpenAI-compatible path.
            # Some Groq account/proxy configurations return 404 for it; retry only in
            # that case through the compatible Responses API.
            if response.status_code == 404:
                response = requests.post(
                    self.RESPONSES_URL,
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json={"model": self.model, "input": messages, "temperature": 0.3, "max_output_tokens": 1200},
                    timeout=90,
                )
                response.raise_for_status()
                return self._responses_text(response.json())
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            detail = ""
            if exc.response is not None:
                # The API's JSON error is actionable; never include request headers or keys.
                detail = f" Details: {exc.response.text[:500]}"
            raise RuntimeError(f"Groq request failed: {exc}.{detail}") from exc
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Groq returned no assistant text. Check GROQ_MODEL_NAME and your API key.") from exc
        if not content:
            raise RuntimeError("Groq returned an empty response.")
        return str(content)

    @staticmethod
    def _responses_text(data: dict) -> str:
        """Extract text from Groq's OpenAI-compatible Responses API shape."""
        if data.get("output_text"):
            return str(data["output_text"])
        parts = []
        for output in data.get("output", []):
            for content in output.get("content", []) if isinstance(output, dict) else []:
                if isinstance(content, dict) and content.get("text"):
                    parts.append(str(content["text"]))
        if not parts:
            raise RuntimeError("Groq Responses API returned no assistant text.")
        return "\n".join(parts)
