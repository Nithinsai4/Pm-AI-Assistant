import streamlit as st
from openai import OpenAI
import pandas as pd
import time
import fitz  # PyMuPDF for PDF reading

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page setup
st.set_page_config(page_title="PM Assistant", layout="wide")
st.title("🤖 AI Assistant for Project Managers")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "last_reply" not in st.session_state:
    st.session_state.last_reply = ""

# ----------------------------
# 1. PDF Upload & Summarization
# ----------------------------
st.sidebar.header("📄 Upload Project Docs")
pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if pdf_file is not None:
    pdf_text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        pdf_text += page.get_text()

    with st.spinner("Summarizing PDF..."):
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this document for a project manager."},
                {"role": "user", "content": pdf_text}
            ],
            temperature=0.3
        )
        st.session_state.summary = summary_response.choices[0].message.content
        st.success("✅ Document summarized.")

# Show summary
if st.session_state.summary:
    st.subheader("📋 Summary of Uploaded Document")
    st.markdown(st.session_state.summary)

    # ----------------------------
    # 2. Task Generator from Summary
    # ----------------------------
    with st.expander("🧩 Generate Tasks from Summary"):
        if st.button("Generate Tasks"):
            with st.spinner("Generating tasks..."):
                task_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Extract clear, actionable project tasks from this summary."},
                        {"role": "user", "content": st.session_state.summary}
                    ],
                    temperature=0.3
                )
                st.markdown("### ✅ Tasks")
                st.markdown(task_response.choices[0].message.content)

# ----------------------------
# 3. AI Chat Assistant
# ----------------------------
st.divider()
st.header("💬 Ask the Assistant")

user_input = st.text_input("What do you need help with today?", placeholder="e.g., How do I write a stakeholder update?")

if st.button("Ask Assistant") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an internal project management assistant. Be concise and helpful."},
                    *st.session_state.messages
                ],
                temperature=0.4
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.last_reply = reply  # ✅ Save for feedback
            st.session_state.history.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "question": user_input,
                "response": reply
            })
        except Exception as e:
            reply = f"Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.last_reply = reply

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------
# 4. Feedback Loop (Fixed)
# ----------------------------
st.markdown("---")
st.subheader("📣 Was this answer helpful?")
feedback = st.radio("Feedback", ["👍 Yes", "👎 No"], horizontal=True)
comments = st.text_area("Any comments or suggestions?")

if st.button("Submit Feedback"):
    question = user_input if user_input else "N/A"
    response = st.session_state.get("last_reply", "No assistant reply available.")
    
    feedback_data = pd.DataFrame.from_records([{
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "response": response,
        "feedback": feedback,
        "comments": comments
    }])
    feedback_data.to_csv("feedback_log.csv", mode="a", index=False, header=False)
    st.success("✅ Feedback recorded. Thanks!")

# ----------------------------
# 5. Chat History & Dashboard
# ----------------------------
st.divider()
st.header("📊 Assistant Interaction Log")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
