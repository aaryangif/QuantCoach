import os
import re

import streamlit as st
from dotenv import load_dotenv

from utils.backboard_client import BackboardMemoryClient
from utils.elevenlabs_client import ElevenLabsClient
from utils.groq_client import GroqClient
from utils.icons import icon_badge, lucide_icon, section_header_html
from utils.mongodb_client import MongoStore
from utils.prompts import (
    ALPHA_GENERATOR_PROMPT,
    GENERAL_COACH_PROMPT,
    LEARNING_PROMPT,
    build_groq_messages,
    extract_tts_summary,
)

load_dotenv()
st.set_page_config(
    page_title="QuantCoach | WorldQuant BRAIN",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

      #MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="stDeployButton"], .stDeployButton, [data-testid="stToolbarActions"] {display: none !important;}
      [data-testid="stHeader"] {background: transparent !important;}
      [data-testid="stSidebarCollapsedControl"], [data-testid="stSidebarCollapseButton"] {display: none !important; visibility: hidden !important; opacity: 0 !important;}

      /* Base Canvas - Warm Almond / Beige Theme */
      .stApp {
        background-color: #FAF7F2;
        color: #1C1917;
        font-family: 'Plus Jakarta Sans', ui-sans-serif, system-ui, -apple-system, sans-serif;
      }

      /* Sidebar - Warm Sand / Linen */
      [data-testid="stSidebar"] {
        background-color: #F3ECE2 !important;
        border-right: 1px solid #E5DACF !important;
      }
      [data-testid="stSidebar"] * {
        font-family: 'Plus Jakarta Sans', ui-sans-serif, system-ui, sans-serif;
        color: #1C1917;
      }
      [data-testid="stSidebar"] .stSelectbox label {
        color: #57534E !important;
        font-weight: 600;
      }

      .block-container {
        max-width: 1260px;
        padding-top: 1.25rem;
        padding-bottom: 3.5rem;
      }

      h1, h2, h3, h4, h5, h6 {
        color: #1C1917;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
      }
      p, label, .stMarkdown {
        color: #292524;
      }

      /* Navigation Brand */
      .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
      }
      .nav-logo-box {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(153, 27, 27, 0.12) 0%, rgba(185, 28, 28, 0.06) 100%);
        border: 1.5px solid rgba(153, 27, 27, 0.28);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(153, 27, 27, 0.08);
      }
      .nav-brand-text {
        display: flex;
        flex-direction: column;
      }
      .brand-name {
        font-weight: 800;
        font-size: 1.2rem;
        color: #1C1917;
        letter-spacing: -0.03em;
        line-height: 1.1;
      }
      .brand-tag {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #991B1B;
        background: #FEF2F2;
        border: 1px solid rgba(153, 27, 27, 0.2);
        border-radius: 4px;
        padding: 1px 6px;
        margin-top: 3px;
        display: inline-block;
        width: fit-content;
      }

      /* Section Headers with Lucide Icon Badges */
      .section-header-block {
        margin-bottom: 1.1rem;
      }
      .section-heading {
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .section-icon-wrap {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: rgba(153, 27, 27, 0.08);
        border: 1.5px solid rgba(153, 27, 27, 0.22);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }
      .section-heading h2 {
        margin: 0;
        font-size: 1.35rem;
        font-weight: 700;
        color: #1C1917;
        letter-spacing: -0.02em;
      }
      .section-subtitle {
        margin: 0.35rem 0 0 50px;
        font-size: 0.88rem;
        color: #78716C;
        line-height: 1.45;
      }

      /* Hero Section */
      .hero-wrap {
        margin: 1.2rem 0 2rem;
        padding: 0.4rem 0;
      }
      .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(153, 27, 27, 0.07);
        border: 1px solid rgba(153, 27, 27, 0.22);
        color: #8B1E22;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 9999px;
        margin-bottom: 0.65rem;
      }
      .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin: 0.25rem 0 0.6rem;
        color: #1C1917;
        line-height: 1.18;
      }
      .hero-title .crimson-accent {
        background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 50%, #DC2626 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
      .hero-copy {
        color: #57534E;
        font-size: 1.05rem;
        max-width: 720px;
        line-height: 1.6;
        margin: 0;
      }

      /* Warm Porcelain Glass Cards */
      .glass-card {
        background: #FFFFFF;
        border: 1px solid #E8DFD5;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px -2px rgba(60, 45, 35, 0.05), 0 2px 6px -1px rgba(60, 45, 35, 0.03);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
      }
      .glass-card:hover {
        box-shadow: 0 8px 28px -4px rgba(60, 45, 35, 0.08), 0 4px 10px -2px rgba(153, 27, 27, 0.04);
      }

      /* Response Card Specifics */
      .response-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.85rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid #F0E8DF;
      }
      .response-header h4 {
        margin: 0;
        color: #8B1E22;
        font-size: 1.15rem;
        font-weight: 700;
      }
      .expression-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #FEF3C7;
        border: 1px solid #FCD34D;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.5rem;
      }
      .audio-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #8B1E22;
        margin: 0.9rem 0 0.35rem;
      }

      /* Buttons: Primary Deep Crimson, Secondary Warm White */
      button[kind="primary"], .stButton > button[kind="primary"], div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #8B1E22 0%, #B91C1C 60%, #DC2626 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #7F1D1D !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.58rem 1.15rem !important;
        box-shadow: 0 4px 14px rgba(153, 27, 27, 0.25) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
      }
      button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover {
        transform: translateY(-1.5px) !important;
        box-shadow: 0 8px 22px rgba(153, 27, 27, 0.35) !important;
        color: #FFFFFF !important;
      }

      button[kind="secondary"], .stButton > button[kind="secondary"], div[data-testid="stButton"] > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #292524 !important;
        border: 1.5px solid #E5DACF !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.58rem 1.15rem !important;
        box-shadow: 0 2px 6px rgba(60, 45, 35, 0.04) !important;
        transition: all 0.15s ease !important;
      }
      button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {
        border-color: #991B1B !important;
        color: #991B1B !important;
        background: #FEF2F2 !important;
      }

      /* Input & Textarea Elements */
      .stTextArea textarea, .stTextInput input {
        background-color: #FAF7F2 !important;
        color: #1C1917 !important;
        border: 1.5px solid #D6CBC0 !important;
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
      }
      .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #991B1B !important;
        box-shadow: 0 0 0 3px rgba(153, 27, 27, 0.14) !important;
      }
      .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #8C827A !important;
      }

      /* Code Blocks - Sleek Dark Espresso */
      [data-testid="stCodeBlock"] {
        border-radius: 12px !important;
        border: 1px solid #3E3835 !important;
        background: #1C1917 !important;
        box-shadow: 0 4px 16px rgba(28, 25, 23, 0.15);
      }
      [data-testid="stCodeBlock"] code {
        font-family: 'JetBrains Mono', monospace !important;
        color: #FAF7F2 !important;
      }

      /* Checkbox & Audio Inputs */
      .stCheckbox label span {
        color: #292524 !important;
        font-weight: 500 !important;
      }
      .stCheckbox [data-testid="stCheckbox"] input:checked + div {
        background-color: #991B1B !important;
        border-color: #991B1B !important;
      }

      /* Architecture & Metric Cards */
      .arch-card {
        background: #FFFFFF;
        border: 1.5px solid #E8DFD5;
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0 4px 16px -2px rgba(60, 45, 35, 0.04);
        height: 100%;
        transition: all 0.2s ease;
      }
      .arch-card:hover {
        border-color: #991B1B;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px -3px rgba(153, 27, 27, 0.1);
      }
      .arch-icon-wrap {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        background: rgba(153, 27, 27, 0.08);
        border: 1px solid rgba(153, 27, 27, 0.22);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.8rem;
      }
      .arch-label {
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        color: #78716C;
        margin-bottom: 0.25rem;
      }
      .arch-value {
        font-size: 1.18rem;
        font-weight: 700;
        color: #1C1917;
        margin-bottom: 0.35rem;
      }
      .arch-desc {
        font-size: 0.85rem;
        color: #57534E;
        line-height: 1.45;
      }

      /* Alpha Risk Pillar Cards */
      .risk-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 12px;
        margin-top: 1rem;
      }
      .risk-item {
        background: #FAF7F2;
        border: 1px solid #E5DACF;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        display: flex;
        gap: 10px;
        align-items: flex-start;
      }
      .risk-title {
        font-size: 0.84rem;
        font-weight: 700;
        color: #1C1917;
      }
      .risk-desc {
        font-size: 0.78rem;
        color: #78716C;
        margin-top: 2px;
        line-height: 1.35;
      }

      /* Top Navigation Bar */
      div[data-testid="stHorizontalBlock"]:has(button[key^="nav_"]) {
        align-items: center;
      }

      /* Footer */
      .footer-note {
        text-align: center;
        color: #8C827A;
        font-size: 0.84rem;
        padding: 2.5rem 0 0.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    defaults = {
        "history": [],
        "backboard_assistant_id": os.getenv("BACKBOARD_ASSISTANT_ID") or None,
        "last_response": None,
        "last_tts": None,
        "last_interaction_id": None,
        "last_section": None,
        "page": "coach",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


@st.cache_resource(show_spinner=False)
def get_store() -> MongoStore:
    return MongoStore()


def mock_mode() -> bool:
    return os.getenv("MOCK_MODE", "false").lower() in {"1", "true", "yes"}


def detect_weak_spot(section: str, question: str) -> str:
    text = question.lower()
    categories = {
        "DSA": ["algorithm", "array", "tree", "graph", "dynamic programming", "complexity"],
        "Math": ["probability", "calculus", "linear algebra", "matrix", "statistics"],
        "Alpha research": ["alpha", "factor", "signal", "expression", "turnover"],
    }
    return next((name for name, words in categories.items() if any(word in text for word in words)), section)


def mock_answer(section: str, question: str) -> str:
    return (
        f"**Mock mode response — {section}**\n\nYou asked: {question}\n\n"
        "This preview confirms the coaching flow without calling external services.\n\n"
        "TTS_SUMMARY: Mock mode is enabled. Add your API keys to use live coaching."
    )


def extract_alpha_expression(answer: str) -> str | None:
    match = re.search(r"(?im)^\s*EXPRESSION:\s*`?([^`\n]+)`?\s*$", answer)
    return match.group(1).strip() if match else None


def handle_api_error(message: str = "Connection issue. Please try again.") -> None:
    st.error(message)


def run_coaching(section: str, question: str, system_prompt: str, make_audio: bool) -> None:
    question = question.strip()
    if not question:
        st.warning("Enter a question or transcribe a recording first.")
        return

    use_mock = mock_mode()
    memory_client = None
    memory_context = ""
    answer = None
    tts_summary = ""

    try:
        with st.spinner("Analyzing quantitative concepts..."):
            if not use_mock:
                try:
                    memory_client = BackboardMemoryClient()
                    if memory_client.api_key:
                        memory_context = memory_client.retrieve_context(st.session_state.backboard_assistant_id)
                except Exception:
                    handle_api_error()
                    return

            try:
                raw_answer = mock_answer(section, question) if use_mock else GroqClient().chat(
                    build_groq_messages(system_prompt, question, st.session_state.history, memory_context)
                )
            except Exception:
                handle_api_error()
                return

            answer, tts_summary = extract_tts_summary(raw_answer)
            st.session_state.history.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer},
            ])
            st.session_state.last_response = answer
            st.session_state.last_section = section
            st.session_state.last_interaction_id = get_store().save_interaction(
                section, question, answer, detect_weak_spot(section, question)
            )

            if not use_mock and memory_client and memory_client.api_key:
                try:
                    st.session_state.backboard_assistant_id = memory_client.save_interaction(
                        question, answer, st.session_state.backboard_assistant_id
                    )
                except Exception:
                    pass

        st.session_state.last_tts = None
        if make_audio and not use_mock:
            with st.spinner("Synthesizing clear audio response..."):
                try:
                    st.session_state.last_tts = ElevenLabsClient().synthesize(tts_summary)
                except Exception:
                    st.warning("Audio is temporarily unavailable, but your answer is ready.")
        elif make_audio and use_mock:
            st.info("Mock mode skips live audio generation.")
    except Exception:
        handle_api_error()


def response_panel(section: str) -> None:
    if not st.session_state.last_response or st.session_state.last_section != section:
        return
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    sparkle_icon = lucide_icon("sparkles", size=18, color="#991B1B")
    st.markdown(f'<div class="response-header">{sparkle_icon}<h4>QuantCoach Insights</h4></div>', unsafe_allow_html=True)
    if section == "Alpha Generator":
        expression = extract_alpha_expression(st.session_state.last_response)
        if expression:
            code_icon = lucide_icon("code-2", size=15, color="#92400E")
            st.markdown(
                f'<div class="expression-badge">{code_icon}<span>Candidate BRAIN-style Fast Expression</span></div>',
                unsafe_allow_html=True,
            )
            st.code(expression, language="python")
    st.markdown(st.session_state.last_response)
    if st.session_state.last_tts:
        audio_icon = lucide_icon("volume-2", size=16, color="#991B1B")
        st.markdown(f'<div class="audio-badge">{audio_icon}<span>Voice Summary (ElevenLabs)</span></div>', unsafe_allow_html=True)
        st.audio(st.session_state.last_tts, format="audio/mpeg")
    left, right = st.columns(2)
    with left:
        if st.button("Helpful", key=f"up_{section}", use_container_width=True):
            saved = get_store().set_rating(st.session_state.last_interaction_id, 1)
            st.success("Feedback recorded.") if saved else st.info("Thank you for the feedback.")
    with right:
        if st.button("Needs work", key=f"down_{section}", use_container_width=True):
            saved = get_store().set_rating(st.session_state.last_interaction_id, -1)
            st.success("Weak-spot logged for review.") if saved else st.info("Thank you for the feedback.")
    st.markdown("</div>", unsafe_allow_html=True)


def voice_input() -> str | None:
    mic_icon = lucide_icon("mic", size=16, color="#991B1B")
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:6px; font-size:0.86rem; color:#57534E; margin-bottom:6px;">'
        f'{mic_icon}<span>Record your question for speech-to-text transcription (ElevenLabs Scribe).</span></div>',
        unsafe_allow_html=True,
    )
    recording = st.audio_input("Voice question", key="coach_audio")
    if not recording:
        return None
    st.audio(recording)
    if st.button("Transcribe recording", key="transcribe_voice", type="secondary"):
        with st.spinner("Transcribing audio question..."):
            try:
                if mock_mode():
                    st.session_state.voice_transcript = "[Mock transcription] Explain cross-sectional ranking."
                    st.info("Mock mode skips live transcription.")
                else:
                    st.session_state.voice_transcript = ElevenLabsClient().transcribe(recording)
            except Exception:
                handle_api_error()
                st.session_state.voice_transcript = None
    return st.session_state.get("voice_transcript")


def progress_panel(store: MongoStore) -> None:
    chart_icon = lucide_icon("bar-chart-3", size=20, color="#991B1B")
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:8px; margin: 1.5rem 0 0.8rem;">'
        f'{chart_icon}<h4 style="margin:0; font-size:1.15rem; color:#1C1917;">Learning Progress & Weak Spots</h4></div>',
        unsafe_allow_html=True,
    )
    rows = store.progress()
    if rows:
        st.dataframe(
            [{"Review topic": row["_id"], "Interactions": row["attempts"], "Needs-work ratings": row["downvotes"]} for row in rows],
            use_container_width=True,
            hide_index=True,
        )
    else:
        info_icon = lucide_icon("info", size=15, color="#78716C")
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:6px; font-size:0.85rem; color:#78716C; margin-top:4px;">'
            f'{info_icon}<span>Ask questions and rate responses to populate your review plan and weak-spot tracker.</span></div>',
            unsafe_allow_html=True,
        )


def section_heading(icon_name: str, title: str, subtitle: str | None = None) -> None:
    st.markdown(section_header_html(icon_name, title, subtitle, icon_color="#991B1B"), unsafe_allow_html=True)


init_state()
store = get_store()

with st.sidebar:
    settings_icon = lucide_icon("sliders", size=20, color="#991B1B")
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:1rem;">'
        f'{settings_icon}<h3 style="margin:0; font-size:1.15rem; color:#1C1917;">Research Station</h3></div>',
        unsafe_allow_html=True,
    )
    st.selectbox("Voice selection", ["Rachel (ElevenLabs Multilingual)"], disabled=True)
    if st.button("Clear Conversation History", key="clear_conversation", use_container_width=True, type="secondary"):
        st.session_state.history = []
        st.session_state.backboard_assistant_id = os.getenv("BACKBOARD_ASSISTANT_ID") or None
        st.session_state.last_response = None
        st.session_state.last_tts = None
        st.session_state.last_interaction_id = None
        st.session_state.last_section = None
        st.session_state.voice_transcript = None
        st.rerun()

    st.markdown("---")
    shield_icon = lucide_icon("shield-check", size=16, color="#991B1B")
    st.markdown(
        f'<div style="font-size:0.8rem; color:#57534E; line-height:1.5;">'
        f'<div style="display:flex; align-items:center; gap:6px; font-weight:700; color:#1C1917; margin-bottom:4px;">'
        f'{shield_icon}<span>Confidential Research</span></div>'
        f'Alpha hypotheses remain private. Groq inference and Backboard Memory Lite ensure models do not retain your proprietary factor ideas.'
        f'</div>',
        unsafe_allow_html=True,
    )

with st.container(key="top_nav"):
    brand_col, navigation_col, settings_nav = st.columns([2.2, 5.8, 0.9])
    with brand_col:
        brand_icon = lucide_icon("trending-up", size=22, color="#991B1B", stroke_width=2.5)
        st.markdown(
            f'<div class="nav-brand">'
            f'  <div class="nav-logo-box">{brand_icon}</div>'
            f'  <div class="nav-brand-text">'
            f'    <span class="brand-name">QuantCoach</span>'
            f'    <span class="brand-tag">WORLDQUANT BRAIN</span>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with navigation_col:
        coach_nav, learn_nav, alpha_nav, resources_nav, about_nav = st.columns(5)
        pages_config = [
            (coach_nav, "coach", "AI Coach"),
            (learn_nav, "learn", "Learn & Quiz"),
            (alpha_nav, "alpha", "Alpha Gen"),
            (resources_nav, "resources", "Resources"),
            (about_nav, "about", "About Us"),
        ]
        for column, page_key, label in pages_config:
            with column:
                is_active = st.session_state.page == page_key
                btn_type = "primary" if is_active else "secondary"
                if st.button(label, key=f"nav_{page_key}", type=btn_type, use_container_width=True):
                    st.session_state.page = page_key
                    st.rerun()
    with settings_nav:
        if st.button("Settings", key="settings_top", use_container_width=True, type="secondary"):
            st.toast("Station settings are available in the left sidebar.")

sparkle_badge = lucide_icon("sparkles", size=14, color="#991B1B", stroke_width=2.4)
st.markdown(
    f'<div class="hero-wrap">'
    f'  <div class="hero-eyebrow">{sparkle_badge}<span>RESEARCH • DSA • ALPHA DISCOVERY</span></div>'
    f'  <div class="hero-title">Your AI Quant Coach for <span class="crimson-accent">WorldQuant BRAIN</span></div>'
    f'  <p class="hero-copy">Build intuition, validate candidate alpha expressions, and practice deliberate quantitative reasoning in an open, privacy-preserving workstation.</p>'
    f'</div>',
    unsafe_allow_html=True,
)

if st.session_state.page == "coach":
    _, coach_col, _ = st.columns([1, 4.2, 1])
    with coach_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_heading("bot", "Your Research Copilot", "Ask quantitative finance, algorithms, probability, or linear algebra questions.")
        spoken = voice_input()
        prompt = st.text_area(
            "Ask a quant, DSA, or math question",
            value=spoken or "",
            height=130,
            placeholder="Why does cross-sectional z-scoring help before combining factors?",
            key="coach_question",
        )
        make_audio = st.checkbox("Read the concise answer aloud", value=True, key="coach_tts")
        if st.button("Ask QuantCoach", type="primary", key="ask_coach", use_container_width=True):
            run_coaching("Coach", prompt, GENERAL_COACH_PROMPT, make_audio)
        st.markdown("</div>", unsafe_allow_html=True)
        response_panel("Coach")

elif st.session_state.page == "learn":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    section_heading("graduation-cap", "Intuition & Deliberate Practice", "Receive a clear first-principles explanation, worked example, common pitfalls, and a 3-question quiz.")
    topic = st.text_area(
        "What would you like to learn?",
        height=135,
        placeholder="Explain bias-variance tradeoff with a factor-model example.",
        key="learn_question",
    )
    make_audio = st.checkbox("Read the concise answer aloud", value=True, key="learn_tts")
    if st.button("Create My Lesson", type="primary", key="ask_learn"):
        run_coaching("Learn", topic, LEARNING_PROMPT, make_audio)
    st.markdown("</div>", unsafe_allow_html=True)
    response_panel("Learn")
    progress_panel(store)

elif st.session_state.page == "alpha":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    section_heading("line-chart", "Translate Intuition into a Candidate Expression", "Educational ideation only — validate every field/operator in your authorized BRAIN workspace. No performance is guaranteed.")
    idea = st.text_area(
        "Describe the intuition or data relationship",
        height=150,
        placeholder="Combine improving operating margins with a short-term reversal filter while avoiding high volatility.",
        key="alpha_idea",
    )
    make_audio = st.checkbox("Read the concise answer aloud", value=True, key="alpha_tts")
    if st.button("Generate Candidate Expression", type="primary", key="ask_alpha"):
        run_coaching("Alpha Generator", idea, ALPHA_GENERATOR_PROMPT, make_audio)
    st.markdown("</div>", unsafe_allow_html=True)
    response_panel("Alpha Generator")

    shield_icon = lucide_icon("shield-check", size=18, color="#991B1B")
    activity_icon = lucide_icon("activity", size=18, color="#991B1B")
    target_icon = lucide_icon("target", size=18, color="#991B1B")
    alert_icon = lucide_icon("alert-circle", size=18, color="#991B1B")

    st.markdown(
        f'<div class="glass-card" style="margin-top: 1.5rem;">'
        f'  <div style="font-size:0.92rem; font-weight:700; color:#1C1917; margin-bottom:0.6rem;">BRAIN Quantitative Rigor Checklist</div>'
        f'  <div class="risk-grid">'
        f'    <div class="risk-item">'
        f'      <div>{shield_icon}</div>'
        f'      <div><div class="risk-title">Lookahead Leakage</div><div class="risk-desc">Verify point-in-time publication dates for fundamental datasets.</div></div>'
        f'    </div>'
        f'    <div class="risk-item">'
        f'      <div>{activity_icon}</div>'
        f'      <div><div class="risk-title">Turnover & Slippage</div><div class="risk-desc">Mitigate transaction drag through decay smoothing and neutralization.</div></div>'
        f'    </div>'
        f'    <div class="risk-item">'
        f'      <div>{target_icon}</div>'
        f'      <div><div class="risk-title">Overfitting / p-Hacking</div><div class="risk-desc">Avoid extensive parameter fishing across arbitrary lookback windows.</div></div>'
        f'    </div>'
        f'    <div class="risk-item">'
        f'      <div>{alert_icon}</div>'
        f'      <div><div class="risk-title">Sub-Universe Correlation</div><div class="risk-desc">Ensure expression does not simply replicate known industry factors.</div></div>'
        f'    </div>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )

elif st.session_state.page == "resources":
    section_heading("video", "Curated Quantitative Library", "Hand-selected foundations for quant research, data structures, and disciplined factor modeling.")
    video_grid = st.columns(2)
    videos = [
        ("Mathematics with Applications in Finance (MIT 18.S096)", "https://www.youtube.com/watch?v=wvXDB9dMdEo"),
        ("Linear Algebra & Factor Foundations (MIT 18.06)", "https://www.youtube.com/watch?v=J7DzL2_Na80"),
        ("Algorithmic Thinking & Complexity (MIT 6.006)", "https://www.youtube.com/watch?v=HtSuA80QTyo"),
        ("Geometric Intuition for High Dimensions (3Blue1Brown)", "https://www.youtube.com/watch?v=fNk_zzaMoSs"),
    ]
    for index, (title, url) in enumerate(videos):
        with video_grid[index % 2]:
            st.markdown(f'<div class="glass-card" style="padding:1.1rem;">', unsafe_allow_html=True)
            play_icon = lucide_icon("play", size=16, color="#991B1B")
            st.markdown(f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">{play_icon}<h4 style="margin:0; font-size:1.05rem;">{title}</h4></div>', unsafe_allow_html=True)
            st.video(url)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    video_search_icon = lucide_icon("video", size=18, color="#991B1B")
    st.markdown(f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">{video_search_icon}<h4 style="margin:0; font-size:1.05rem;">Watch Custom Lecture or Seminar</h4></div>', unsafe_allow_html=True)
    user_url = st.text_input("Paste a YouTube URL to watch in your workstation:", placeholder="https://www.youtube.com/watch?v=...")
    if user_url:
        st.video(user_url)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "about":
    section_heading("info", "About QuantCoach", "Architected for open-source AI, intellectual property protection, and zero vendor lock-in.")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(
        "QuantCoach is engineered with **open-source AI** at its core. We orchestrate Groq for ultra-low latency open-weight "
        "LLM inference, Backboard for persistent Memory Lite & contextual RAG, and ElevenLabs for natural speech intelligence."
    )
    st.markdown(
        "This decoupled architecture ensures alpha hypotheses remain strictly private, makes the quantitative pipeline "
        "transparent, and eliminates per-user cost barriers. Researchers can iterate freely without being locked into closed, proprietary platforms."
    )
    st.markdown(
        "*Note: QuantCoach is an educational companion for quantitative modeling, DSA, and mathematics. "
        "It supports deliberate practice and research ideation; it does not promise alpha performance, low correlation, or BRAIN platform approval.*"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    stack_a, stack_b, stack_c = st.columns(3)
    cpu_icon = lucide_icon("cpu", size=20, color="#991B1B")
    db_icon = lucide_icon("database", size=20, color="#991B1B")
    vol_icon = lucide_icon("volume-2", size=20, color="#991B1B")

    with stack_a:
        st.markdown(
            f'<div class="arch-card">'
            f'  <div class="arch-icon-wrap">{cpu_icon}</div>'
            f'  <div class="arch-label">Inference Engine</div>'
            f'  <div class="arch-value">Groq LPUs</div>'
            f'  <div class="arch-desc">Ultra-fast open-weight models (Llama, Qwen, Mistral) providing real-time feedback without retaining prompts.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with stack_b:
        st.markdown(
            f'<div class="arch-card">'
            f'  <div class="arch-icon-wrap">{db_icon}</div>'
            f'  <div class="arch-label">Contextual Memory</div>'
            f'  <div class="arch-value">Backboard Memory</div>'
            f'  <div class="arch-desc">Persistent learning facts and weak-spot memory retrieved via lightweight endpoints without routed inference.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with stack_c:
        st.markdown(
            f'<div class="arch-card">'
            f'  <div class="arch-icon-wrap">{vol_icon}</div>'
            f'  <div class="arch-label">Voice Intelligence</div>'
            f'  <div class="arch-value">ElevenLabs</div>'
            f'  <div class="arch-desc">Scribe speech-to-text audio ingestion and multilingual natural speech synthesis for auditory review.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

heart_icon = lucide_icon("flame", size=14, color="#991B1B")
st.markdown(
    f'<div class="footer-note">'
    f'<span>Engineered for Quantitative Researchers</span> • {heart_icon} <span>Open-Source AI Core</span> • <span>Hacktoberfest 2026</span>'
    f'</div>',
    unsafe_allow_html=True,
)
