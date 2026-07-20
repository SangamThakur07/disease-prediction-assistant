"""
Disease Prediction Assistant — Streamlit App
Run with: streamlit run app.py
"""

import pickle
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Disease Prediction Assistant", page_icon="🩺", layout="centered")

# ---------- Load model ----------
@st.cache_resource
def load_model():
    with open("disease_prediction_model.pkl", "rb") as f:
        data = pickle.load(f)
    return data["model"], data["label_encoder"], data["symptoms"], data["model_name"]

model, le, symptoms, model_name = load_model()
diseases = list(le.classes_)


def predict_disease(selected_symptoms, top_k=3):
    vector = np.zeros(len(symptoms))
    for i, s in enumerate(symptoms):
        if s in selected_symptoms:
            vector[i] = 1

    if vector.sum() == 0:
        return None

    proba = model.predict_proba(vector.reshape(1, -1))[0]
    top_idx = np.argsort(proba)[::-1][:top_k]

    return [
        {"disease": diseases[i], "confidence": float(proba[i])}
        for i in top_idx
    ]


# ---------- UI ----------
st.title("🩺 Disease Prediction Assistant")
st.caption(
    "Select the symptoms you're experiencing and get a ranked list of the most "
    "likely conditions, powered by a "
    f"**{model_name}** model trained on {len(symptoms)} symptoms across {len(diseases)} diseases."
)

st.warning(
    "⚠️ **Educational project only.** This tool is not a medical device and does not "
    "provide medical advice. Always consult a qualified healthcare professional for "
    "diagnosis and treatment.",
    icon="⚠️",
)

display_names = [s.replace("_", " ").title() for s in symptoms]
name_map = dict(zip(display_names, symptoms))

selected_display = st.multiselect(
    "Select your symptoms",
    options=sorted(display_names),
    placeholder="Start typing a symptom, e.g. 'Headache', 'Fever'...",
)

selected_symptoms = {name_map[d] for d in selected_display}

col1, col2 = st.columns([1, 1])
with col1:
    predict_clicked = st.button("🔍 Predict Disease", type="primary", use_container_width=True)
with col2:
    clear_clicked = st.button("Clear", use_container_width=True)

if clear_clicked:
    st.rerun()

if predict_clicked:
    if not selected_symptoms:
        st.error("Please select at least one symptom.")
    else:
        results = predict_disease(selected_symptoms, top_k=3)
        st.subheader("Prediction Results")

        top = results[0]
        st.success(f"**Most likely: {top['disease']}**  \nConfidence: {top['confidence']:.1%}")

        if len(results) > 1:
            st.markdown("**Other possibilities:**")
            for r in results[1:]:
                st.write(f"- {r['disease']} — {r['confidence']:.1%}")

        st.markdown("---")
        st.caption(
            "Based on symptoms: " + ", ".join(sorted(s.replace('_', ' ') for s in selected_symptoms))
        )

with st.expander("ℹ️ About this project"):
    st.markdown(
        f"""
        This assistant uses a **{model_name}** classifier trained on the
        [Disease Prediction Using Machine Learning](https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning)
        dataset (132 symptoms → 41 diseases).

        See `Disease_Prediction_Assistant.ipynb` for the full data exploration,
        model comparison, and evaluation.
        """
    )
