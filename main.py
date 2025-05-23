import streamlit as st
import requests
import json

# Title aur styling
st.set_page_config(page_title="AI Questions | Answers", page_icon="🤖", layout="centered")
st.title("🤖 AI Questions | Answers")
st.markdown("write your question and get answer from AI!")

# Sidebar: API Key input
st.sidebar.title("🔐 API Settings")
api_key = st.sidebar.text_input("OpenRouter API Key", type="password", value="your-api-key-here")

# Model selection
model = st.sidebar.selectbox("Select Model ", [
     "mistralai/devstral-small:free",
    "qwen/qwen3-30b-a3b:free",
    "google/gemini-1.5-flash",
    "meta-llama/llama-3-8b-instruct:free",
    "mistralai/mixtral-8x7b-instruct",
   

])

# Input field for user's question
user_question = st.text_area("✍️ write your question.", height=150)

# Button to submit
if st.button("🔍 Answer."):
    if not api_key:
        st.error("❗ First put API key in sidebar.")
    elif not user_question.strip():
        st.warning("❗ Question.")
    else:
        # API call
        BASE_URL = "https://openrouter.ai/api/v1"

        with st.spinner("🤖 Thinking..."):
            response = requests.post(
                url=f"{BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": user_question
                        }
                    ]
                })
            )

            if response.status_code == 200:
                reply = response.json()['choices'][0]['message']['content']
                st.success("✅ AI Answer:")
                st.markdown(reply) 
            else:
                st.error(f"❌ Error {response.status_code}")
                st.text(response.text)
