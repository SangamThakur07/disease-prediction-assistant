import streamlit as st
from utils import (
    page_setup, pulse_divider, disclaimer_banner,
    load_model, predict_disease, PRIMARY, MUTED,
)
from disease_data import DISEASE_INFO

page_setup("Home")
model, le, symptoms, model_name = load_model()
diseases = list(le.classes_)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown('<div class="hero-eyebrow">AI/ML SYMPTOM ASSISTANT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Describe what you feel.<br>We\'ll narrow it down.</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-sub">Diagnos.ai compares your symptoms against patterns learned '
    f'from {len(symptoms)} known symptoms across {len(diseases)} conditions, powered by a '
    f'{model_name} model, and ranks the most likely matches with a confidence score.</div>',
    unsafe_allow_html=True,
)
pulse_divider()
disclaimer_banner()

# ---------------------------------------------------------------------------
# Symptom picker
# ---------------------------------------------------------------------------
st.markdown("#### Select your symptoms")

display_names = sorted(s.replace("_", " ").title() for s in symptoms)
name_map = {s.replace("_", " ").title(): s for s in symptoms}

selected_display = st.multiselect(
    "Type to search symptoms",
    options=display_names,
    placeholder="e.g. Headache, High Fever, Fatigue...",
    label_visibility="collapsed",
)

st.caption(f"{len(selected_display)} symptom(s) selected")

selected_symptoms = {name_map[d] for d in selected_display}

col1, col2 = st.columns([1, 1])
with col1:
    predict_clicked = st.button("🔍 Analyze symptoms", type="primary", width='stretch')
with col2:
    clear_clicked = st.button("Clear selection", width='stretch')

if clear_clicked:
    st.rerun()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if predict_clicked:
    if not selected_symptoms:
        st.error("Please select at least one symptom before analyzing.")
    else:
        results = predict_disease(model, le, symptoms, selected_symptoms, top_k=3)
        top = results[0]
        conf_pct = top["confidence"] * 100

        st.markdown("#### Result")
        st.markdown(
            f"""
            <div class="card">
                <div class="hero-eyebrow">MOST LIKELY MATCH</div>
                <div class="result-disease">{top['disease']}</div>
                <div class="confidence-track">
                    <div class="confidence-fill" style="width:{conf_pct:.1f}%;"></div>
                </div>
                <div style="color:{MUTED}; font-size:0.85rem;">{conf_pct:.1f}% confidence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if len(results) > 1:
            st.markdown("**Other possibilities:**")
            tag_html = "".join(
                f'<span class="tag">{r["disease"]} · {r["confidence"]*100:.0f}%</span>'
                for r in results[1:]
            )
            st.markdown(tag_html, unsafe_allow_html=True)

        info = DISEASE_INFO.get(top["disease"])
        if info:
            with st.expander(f"General info & precautions for {top['disease'].strip()}"):
                st.markdown(f"**{info['category']}**")
                st.write(info["overview"])
                st.markdown("**General precautions:**")
                for p in info["precautions"]:
                    st.markdown(f"- {p}")
                st.caption(f"See a doctor if: {info['see_doctor_if']}")
                st.page_link("pages/2_Disease_Library.py", label="View full Disease Library →")

        st.caption(
            "Based on: " + ", ".join(sorted(s.replace("_", " ").title() for s in selected_symptoms))
        )
