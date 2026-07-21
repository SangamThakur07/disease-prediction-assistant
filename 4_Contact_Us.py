import streamlit as st
from utils import page_setup, pulse_divider

page_setup("About Us")

st.markdown('<div class="hero-eyebrow">THE PROJECT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">About Diagnos.ai</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">A student-built machine learning project exploring how far '
    'a simple symptom checklist can go toward narrowing down a likely diagnosis.</div>',
    unsafe_allow_html=True,
)
pulse_divider()

st.markdown(
    """
    <div class="card">
    <b>Why we built this</b><br><br>
    Most people's first instinct when they feel unwell is to search their symptoms online —
    often landing on inconsistent or alarmist results. This project explores whether a
    transparent, trained-from-scratch classifier can do a more consistent job of ranking
    likely conditions from a set of reported symptoms, while being upfront about its
    limitations.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### What's under the hood")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Data**")
    st.caption("4,920 labeled patient records, 132 symptoms, 41 diseases")
with c2:
    st.markdown("**Model**")
    st.caption("Compared 5 classifiers via 5-fold cross-validation")
with c3:
    st.markdown("**Interface**")
    st.caption("Interactive Streamlit assistant + disease reference library")

st.markdown("#### Project scope & honesty")
st.markdown(
    """
    <div class="card">
    This is an <b>educational AI/ML submission</b>, not a certified medical product.
    The dataset used here has clean, well-separated symptom patterns per disease, which is
    why the model reports very high accuracy — a real clinical tool would need to handle
    messier, overlapping, real-world symptom data, larger and more diverse populations,
    and rigorous clinical validation before ever being trusted with real decisions.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### Built with")
tags = ["Python", "scikit-learn", "Pandas", "Streamlit", "Matplotlib / Seaborn"]
st.markdown("".join(f'<span class="tag">{t}</span>' for t in tags), unsafe_allow_html=True)
