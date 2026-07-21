"""Shared helpers for the Diagnos.ai multi-page Streamlit app."""

import pickle
import numpy as np
import streamlit as st

# ---------------------------------------------------------------------------
# Design tokens — "clinical pulse" identity
# ---------------------------------------------------------------------------
INK = "#132A26"
PAPER = "#F1F5F3"
SURFACE = "#FFFFFF"
PRIMARY = "#0F6B5C"       # deep pine/teal — trust, clinical calm
PRIMARY_DARK = "#0A4A40"
ACCENT = "#E4572E"        # coral pulse — used sparingly for CTAs/alerts
MUTED = "#5B6F6A"
LINE = "#DCE6E2"
GOLD = "#C99A3E"          # warm highlight for confidence/rank accents


def inject_theme():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{
            font-family: 'IBM Plex Sans', sans-serif;
        }}

        .stApp {{
            background: {PAPER};
        }}

        h1, h2, h3, .display-font {{
            font-family: 'Fraunces', serif !important;
            color: {INK} !important;
            letter-spacing: -0.01em;
        }}

        p, li, span, label, div {{
            color: {INK};
        }}

        section[data-testid="stSidebar"] {{
            background: {SURFACE};
            border-right: 1px solid {LINE};
        }}

        /* Hero */
        .hero-eyebrow {{
            font-family: 'IBM Plex Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-size: 0.72rem;
            color: {PRIMARY};
            font-weight: 500;
        }}
        .hero-title {{
            font-family: 'Fraunces', serif;
            font-size: 2.6rem;
            font-weight: 600;
            color: {INK};
            line-height: 1.08;
            margin: 0.3rem 0 0.6rem 0;
        }}
        .hero-sub {{
            font-size: 1.05rem;
            color: {MUTED};
            max-width: 640px;
            line-height: 1.55;
        }}

        /* Pulse divider — signature element */
        .pulse-divider {{
            width: 100%;
            height: 34px;
            margin: 1.4rem 0 1.6rem 0;
        }}

        /* Disclaimer banner */
        .disclaimer {{
            background: #FCEFEA;
            border-left: 3px solid {ACCENT};
            padding: 0.7rem 1rem;
            border-radius: 4px;
            font-size: 0.86rem;
            color: {INK};
            margin: 0.8rem 0 1.4rem 0;
        }}

        /* Cards */
        .card {{
            background: {SURFACE};
            border: 1px solid {LINE};
            border-radius: 10px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
        }}
        .tag {{
            display: inline-block;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            background: {PAPER};
            border: 1px solid {LINE};
            color: {MUTED};
            padding: 0.15rem 0.55rem;
            border-radius: 999px;
            margin: 0.15rem 0.3rem 0.15rem 0;
        }}

        /* Result card */
        .result-disease {{
            font-family: 'Fraunces', serif;
            font-size: 1.9rem;
            font-weight: 600;
            color: {PRIMARY_DARK};
            margin-bottom: 0.2rem;
        }}
        .confidence-track {{
            background: {LINE};
            border-radius: 999px;
            height: 10px;
            width: 100%;
            overflow: hidden;
            margin: 0.4rem 0 0.2rem 0;
        }}
        .confidence-fill {{
            background: linear-gradient(90deg, {PRIMARY} 0%, {GOLD} 100%);
            height: 100%;
            border-radius: 999px;
        }}

        /* Buttons */
        .stButton > button {{
            background: {PRIMARY};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.55rem 1.3rem;
            font-weight: 600;
            transition: background 0.15s ease;
        }}
        .stButton > button:hover {{
            background: {PRIMARY_DARK};
            color: white;
        }}

        footer {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def pulse_divider():
    st.markdown(
        f"""
        <svg class="pulse-divider" viewBox="0 0 700 34" xmlns="http://www.w3.org/2000/svg">
          <polyline points="0,17 220,17 245,17 260,4 275,30 292,17 320,17 340,17 355,2 372,32 390,17 700,17"
            fill="none" stroke="{ACCENT}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        unsafe_allow_html=True,
    )


def disclaimer_banner(text=None):
    text = text or (
        "This is an educational student ML project, not a medical device. "
        "It does not diagnose disease — always consult a licensed healthcare "
        "professional for medical advice."
    )
    st.markdown(f'<div class="disclaimer">⚠️ {text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
@st.cache_resource
def load_model():
    with open("disease_prediction_model.pkl", "rb") as f:
        data = pickle.load(f)
    return data["model"], data["label_encoder"], data["symptoms"], data["model_name"]


def predict_disease(model, le, symptoms, selected_symptoms, top_k=3):
    diseases = list(le.classes_)
    vector = np.zeros(len(symptoms))
    for i, s in enumerate(symptoms):
        if s in selected_symptoms:
            vector[i] = 1

    if vector.sum() == 0:
        return None

    proba = model.predict_proba(vector.reshape(1, -1))[0]
    top_idx = np.argsort(proba)[::-1][:top_k]
    return [{"disease": diseases[i], "confidence": float(proba[i])} for i in top_idx]


def page_setup(title):
    st.set_page_config(page_title=f"{title} · Diagnos.ai", page_icon="🩺", layout="centered")
    inject_theme()
