import os
import requests
import streamlit as st
import uuid

st.set_page_config(page_title="My Resume + Chatbot", layout="wide")

N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", os.getenv("N8N_WEBHOOK_URL", ""))

# --- NEW: session id generator (for n8n Simple Memory) ---
def get_session_id() -> str:
    """Create a stable session id for the current Streamlit session."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

# 1) Your resume content (start simple: paste text here)
RESUME_TEXT = """
NAME: Maverix ...
SUMMARY: ...
EXPERIENCE:
- Role, Company, Dates: ...
PROJECTS:
- ...
SKILLS: ...
"""

# --- Layout ---
left, right = st.columns([2, 1], gap="large")

with left:
    st.title("Maverix — Resume")
    st.subheader("Summary")
    st.write("...your summary here...")

    st.subheader("Experience")
    st.write("...your experience here...")

    st.subheader("Projects")
    st.write("...your projects here...")

    st.subheader("Skills")
    st.write("...your skills here...")

with right:
    st.header("Ask my resume")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    prompt = st.chat_input("Ask a question about my background...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        payload = {
            "sessionId": get_session_id(),               # <-- NEW: required for Simple Memory
            "question": prompt,
            "resume_text": RESUME_TEXT,
            "history": st.session_state.messages[-10:],  # optional
        }

        try:
            r = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)

            # OPTIONAL DEBUG (uncomment if you want to see what's happening)
            # st.caption(f"HTTP {r.status_code}")
            # st.code(r.text)

            r.raise_for_status()
            data = r.json()

            # Prefer reply; if absent, show full JSON for visibility
            reply = data.get("reply") or data.get("text") or str(data)

        except Exception as e:
            reply = f"Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
