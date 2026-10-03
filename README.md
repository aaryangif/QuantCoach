# QuantCoach: Your AI Quant Coach for WorldQuant BRAIN

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.65+-FF4B4B.svg)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Inference-Groq%20LPU-orange.svg)](https://groq.com)

[🚀 Try the Live Demo](https://quantcoach.onrender.com) · [📖 Read the DEV post](https://dev.to)

QuantCoach is a focused, open-source AI learning assistant for quantitative finance, data structures, mathematics, and WorldQuant BRAIN-style alpha research. It helps a quant friend learn faster, practice with feedback, and explore candidate ideas in a structured, private, and cost-free workspace.

---

## Built for a friend

I built this specifically for my friend, who is preparing for WorldQuant BRAIN and learning quantitative research from the ground up. Their biggest friction points were:

- Losing track of *why* previous alpha ideas failed
- Not having a fast way to test intuition against fundamentals (probability, linear algebra, DSA)
- Repeating the same mistakes because nothing remembered their weak spots

After handing it over, they said:

> *"The weak-spot tracker alone saved me hours of re-reading old notes. And asking follow-up questions out loud while I'm sketching ideas is way better than typing."*

That quote is the whole reason this exists.

---

## The problem it solves

Many self-directed quant learners struggle to:

- Build DSA fundamentals and algorithmic intuition
- Refresh probability, statistics, and linear algebra on demand
- Generate disciplined alpha ideas without drifting into overfitting
- Turn mistakes into a durable review loop instead of forgetting them

QuantCoach makes that process conversational, voice-enabled, and lightweight. Ask a question in plain language, speak it aloud, and get structured coaching back — plus an active memory of where you've struggled before.

---

## Open-source AI architecture

QuantCoach is built on an open, decoupled, and modular stack:

- **Groq** — Ultra-low-latency open-weight model inference (Llama, Qwen, GPT-OSS family) on LPUs
- **Backboard** — Persistent Memory Lite for conversational context and weak-spot recall (without routed LLM inference)
- **ElevenLabs** — Scribe speech-to-text audio ingestion and multilingual natural text-to-speech
- **Streamlit** — The entire interface layer and workstation chrome
- **MongoDB Atlas** *(optional)* — Unlocks persistent cross-session progress tracking and the weak-spot analytics dashboard (with automatic in-memory fallback if not configured)

---

## Why open source matters here

1. **Privacy of alpha ideas.** Alpha hypotheses are proprietary intellectual property. Running open-weight models through Groq and storing memory in Backboard means your research context never trains a closed commercial model.
2. **Model portability.** If a better open-weight model ships tomorrow, you change one line in `.env` (`GROQ_MODEL_NAME`) — no code rewrite, zero vendor lock-in.
3. **Zero cost to the learner.** The entire stack runs on free tiers. Quantitative education shouldn't require a $20/month proprietary subscription.

---

## Features

- **🤖 AI Coach** — Ask quant, DSA, or math questions in text or voice. Get structured answers with first-principles explanations and worked examples.
- **📚 Learn & Quiz** — First-principles explanations, common pitfalls, and a 3-question quiz per topic. Your weak spots and review topics are tracked in real time.
- **📈 Alpha Generator** — Translate intuition into a candidate BRAIN-style Fast Expression, with a quantitative rigor checklist (lookahead leakage, turnover drag, overfitting/p-hacking, correlation).
- **🎥 Resources** — Curated quantitative learning lectures (MIT 18.S096 Finance, MIT 18.06 Linear Algebra, MIT 6.006 Algorithms, 3Blue1Brown) embedded directly in the app. Paste any YouTube URL to watch in-place.
- **ℹ️ About** — Architecture overview, technical philosophy, and the open-source rationale.

---

## UI & Editorial Design System

- **Editorial Quant Aesthetic**: Warm almond/beige parchment canvas (`#FAF7F2`) paired with deep burgundy and crimson accents (`#991B1B`, `#8B1E22`, `#DC2626`).
- **Lucide Icon Integration**: Vector SVG icons (`trending-up`, `bot`, `graduation-cap`, `line-chart`, `video`, `code-2`, `mic`, `volume-2`, `shield-check`, `cpu`, `database`) crafted specifically for quantitative workstations.
- **Typography**: Clean Google Fonts pairing `Plus Jakarta Sans` for interface chrome and `JetBrains Mono` for code blocks, mathematical factors, and candidate BRAIN expressions.

---

## Project Structure

```text
quantcoach/
├── .streamlit/
│   ├── config.toml           # Streamlit theme (warm almond / crimson palette)
│   └── credentials.toml      # Headless workstation environment configuration
├── docs/
│   └── screenshots/          # High-resolution architectural and UI vector placeholders
├── utils/
│   ├── __init__.py           # Package exports
│   ├── backboard_client.py   # Backboard Memory Lite retrieval and storage
│   ├── elevenlabs_client.py  # ElevenLabs Scribe STT and multilingual TTS
│   ├── groq_client.py        # Groq LPU inference for open-weight models
│   ├── icons.py              # Lucide SVG vector icon system
│   ├── mongodb_client.py     # MongoDB Atlas persistence (with in-memory fallback)
│   └── prompts.py            # System prompts and TTS summary extraction
├── .env.example              # Environment variable template
├── app.py                    # Main Streamlit application & workstation UI
├── render.yaml               # Cloud deployment specification for Render
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd quantcoach
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Create your environment file

```bash
cp .env.example .env
```

### 4. Fill in your API keys in `.env`

```env
GROQ_API_KEY=your_groq_api_key_here
BACKBOARD_API_KEY=your_backboard_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
GROQ_MODEL_NAME=openai/gpt-oss-120b
# Optional:
MONGODB_URI=your_mongodb_atlas_uri_here
```

### 5. Run the workstation

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---


## Hacktoberfest 2026 Note

This project is prepared for Hacktoberfest 2026 to showcase clean, open-source AI infrastructure that empowers learners with practical quantitative modeling, transparent memory, and complete freedom from vendor lock-in.

---

## License

Distributed under the [MIT License](LICENSE). Educational and research use only. Alpha expressions should be validated in an authorized WorldQuant BRAIN environment before any live deployment or trading decision.
