import os

import requests


DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs Rachel voice.


class ElevenLabsClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise RuntimeError("ELEVENLABS_API_KEY is not configured.")
        return {"xi-api-key": self.api_key}

    def transcribe(self, uploaded_audio) -> str:
        """Send Streamlit's uploaded audio object to ElevenLabs Speech-to-Text."""
        if not uploaded_audio:
            raise ValueError("Record or choose an audio file first.")
        filename = getattr(uploaded_audio, "name", "recording.wav")
        mime_type = getattr(uploaded_audio, "type", "audio/wav")
        try:
            response = requests.post(
                "https://api.elevenlabs.io/v1/speech-to-text", headers=self._headers(),
                files={"file": (filename, uploaded_audio.getvalue(), mime_type)},
                data={"model_id": "scribe_v1"}, timeout=90,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise RuntimeError(f"ElevenLabs transcription failed: {exc}") from exc
        text = data.get("text") or data.get("transcript")
        if not text:
            raise RuntimeError("ElevenLabs returned no transcription.")
        return str(text).strip()

    def synthesize(self, text: str, voice_id: str = DEFAULT_VOICE_ID) -> bytes:
        if not text.strip():
            raise ValueError("There is no text to speak.")
        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers={**self._headers(), "Content-Type": "application/json", "Accept": "audio/mpeg"},
                json={"text": text[:1500], "model_id": "eleven_multilingual_v2",
                      "voice_settings": {"stability": 0.45, "similarity_boost": 0.75}},
                timeout=90,
            )
            response.raise_for_status()
            return response.content
        except requests.RequestException as exc:
            raise RuntimeError(f"ElevenLabs speech generation failed: {exc}") from exc
