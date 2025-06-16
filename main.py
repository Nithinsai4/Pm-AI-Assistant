# pm_ai_assistant/main.py
import streamlit as st
import openai
import pandas as pd
import time

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Or use your own method to load securely

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page setup
st.set_page_config(page_title="PM Assistant", layout="centered")
st.title("🤖 AI Assistant for Project Managers")

st.markdown("Ask me about project risk, stakeholder updates, sprint metrics, and more.")

# User input
user_input = st.text_input("What do you need help with today?", placeholder="e.g., How do I write a stakeholder update?")

# Submit button
if st.button("Ask Assistant") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an internal project management assistant. Answer clearly and practically."},
                    *st.session_state.messages
                ],
                temperature=0.4
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            reply = f"Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Feedback section
st.markdown("---")
st.subheader("Was this answer helpful?")
feedback = st.radio("Feedback", ["👍 Yes", "👎 No"], horizontal=True)
comments = st.text_area("Any comments or suggestions?")

if st.button("Submit Feedback"):
    feedback_data = pd.DataFrame.from_records([
        {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "question": user_input,
            "response": reply,
            "feedback": feedback,
            "comments": comments
        }
    ])
    feedback_data.to_csv("feedback_log.csv", mode="a", index=False, header=False)
    st.success("✅ Feedback recorded. Thanks!")
