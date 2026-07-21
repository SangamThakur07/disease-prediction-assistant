import streamlit as st
from utils import page_setup, pulse_divider

page_setup("Contact Us")

st.markdown('<div class="hero-eyebrow">GET IN TOUCH</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Contact us</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Questions about the project, the dataset, or want to '
    'collaborate? Send a note below.</div>',
    unsafe_allow_html=True,
)
pulse_divider()

with st.form("contact_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your name")
    with col2:
        email = st.text_input("Your email")
    subject = st.text_input("Subject")
    message = st.text_area("Message", height=140)
    submitted = st.form_submit_button("Send message", type="primary")

    if submitted:
        if not name or not email or not message:
            st.error("Please fill in your name, email, and message.")
        else:
            st.success(f"Thanks {name.split()[0] if name else ''} — your message has been noted. We'll get back to you at {email}.")

st.caption(
    "Note: this form is a UI demo for the project submission — messages aren't wired to "
    "a live inbox yet. Replace the form handler with an email/service API call to make it functional."
)

st.markdown("#### Other ways to reach us")
st.markdown(
    """
    <div class="card">
    📧 <b>Email:</b> sangamthakur2aa6@gmail.com<br>
    💻 <b>GitHub:</b> <a href="https://github.com/SangamThakur07" target="_blank">github.com/SangamThakur07</a><br>
    🏫 <b>Institution:</b> Lovely Professional University
    </div>
    """,
    unsafe_allow_html=True,
)
