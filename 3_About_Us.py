import streamlit as st
from utils import page_setup, pulse_divider, disclaimer_banner, MUTED
from disease_data import DISEASE_INFO

page_setup("Disease Library")

st.markdown('<div class="hero-eyebrow">REFERENCE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Disease library</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">General, educational information and everyday precautions '
    'for every condition the assistant can recognize — organized by category.</div>',
    unsafe_allow_html=True,
)
pulse_divider()
disclaimer_banner(
    "This library provides general educational information only, not treatment "
    "instructions. Always consult a licensed healthcare professional."
)

# group by category
categories = {}
for name, info in DISEASE_INFO.items():
    categories.setdefault(info["category"], []).append((name, info))

search = st.text_input("Search a disease", placeholder="e.g. Diabetes, Migraine, Asthma...")

for cat, items in sorted(categories.items()):
    items = sorted(items, key=lambda x: x[0].strip())
    if search:
        items = [it for it in items if search.lower() in it[0].lower()]
        if not items:
            continue

    st.markdown(f"##### {cat}")
    for name, info in items:
        with st.expander(name.strip()):
            st.write(info["overview"])
            st.markdown("**General precautions:**")
            for p in info["precautions"]:
                st.markdown(f"- {p}")
            st.markdown(
                f'<div style="color:{MUTED}; font-size:0.85rem; margin-top:0.4rem;">'
                f'See a doctor if: {info["see_doctor_if"]}</div>',
                unsafe_allow_html=True,
            )
