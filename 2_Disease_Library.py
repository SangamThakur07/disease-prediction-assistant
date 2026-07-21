import streamlit as st
from utils import page_setup, pulse_divider, load_model, MUTED, PRIMARY

page_setup("How It Works")
model, le, symptoms, model_name = load_model()
diseases = list(le.classes_)

st.markdown('<div class="hero-eyebrow">METHODOLOGY</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">How the model works</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-sub">A behind-the-scenes look at the data, the model comparison, '
    f'and why the assistant makes the predictions it does.</div>',
    unsafe_allow_html=True,
)
pulse_divider()

st.markdown("#### 1. The dataset")
st.markdown(
    f"""
    <div class="card">
    Trained on <b>4,920 patient records</b>, each with <b>{len(symptoms)} binary symptom features</b>
    (present / absent) and one of <b>{len(diseases)} disease labels</b>. Every disease has a
    fixed, largely non-overlapping symptom signature — a deliberate design choice in
    curated symptom-checker datasets that keeps classes highly separable.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### 2. Model comparison")
st.markdown(
    "Five algorithms were trained and compared using 5-fold stratified cross-validation: "
    "Decision Tree, Random Forest, Gaussian Naive Bayes, Support Vector Machine, and "
    "Logistic Regression."
)
st.image("assets/model_comparison.png", width='stretch')

col1, col2, col3 = st.columns(3)
col1.metric("Best test accuracy", "100%")
col2.metric("Selected model", model_name)
col3.metric("Cross-val folds", "5")

st.markdown("#### 3. Where the model gets confused (and where it doesn't)")
st.image("assets/confusion_matrix.png", width='stretch')
st.caption("A near-perfect diagonal means the model rarely mixes up diseases on the held-out test set.")

st.markdown("#### 4. Which symptoms matter most")
st.image("assets/feature_importance.png", width='stretch')
st.caption("Highly disease-specific symptoms dominate the model's decisions — this is also why accuracy is so high.")

st.markdown("#### 5. Class balance")
st.image("assets/class_distribution.png", width='stretch')

st.markdown(
    f"""
    <div class="disclaimer">
    ⚠️ The reported accuracy reflects this dataset's clean, synthetic structure —
    not real-world diagnostic performance. Treat this as an educational demonstration
    of the ML workflow, not a validated clinical tool.
    </div>
    """,
    unsafe_allow_html=True,
)
