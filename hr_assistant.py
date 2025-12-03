import streamlit as st
import os
from dotenv import load_dotenv
import google.genai as genai

# Load environment variables from .env when running locally
load_dotenv()

# HR Knowledge Base (hardcoded)
HR_KNOWLEDGE = """
Leave Policy:
- Annual Leave: 21 days per year, pro-rated for first year
- Sick Leave: 7 days per year, medical certificate required after 3 days
- Maternity Leave: 26 weeks paid for female employees
- Paternity Leave: 15 days paid
- Carry forward: Maximum 7 days annual leave

Benefits:
- Health Insurance: Company pays 80%, covers family
- Gratuity: After 5 years service
- Bonus: Performance based, up to 2 months salary

Work Policy:
- Work hours: 9 AM - 6 PM, Monday-Friday
- Remote work: 2 days per week approved
- Overtime: 1.5x rate after 48 hours/week
"""

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found. Add it to your .env file or Streamlit secrets.")
        st.info("Example .env line: GEMINI_API_KEY=your-gemini-key-here")
        st.stop()

    # Configure Gemini client and return a GenerativeModel
    client = genai.Client(api_key=api_key)
    model = client.models.get("gemini-1.5-flash")
    return client, model

def main():
    st.set_page_config(page_title="HR Assistant Agent", layout="wide")
    st.title("🤖 HR Assistant Agent")
    st.markdown("**Roomans AI Challenge - HR Policy Assistant (Gemini-powered)**")

    client, _ = get_model()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar with HR policies
    with st.sidebar:
        st.markdown("### 📋 HR Policies")
        st.code(HR_KNOWLEDGE, language="text")

    # Show previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask about policies, leave, benefits..."):
        # Add and show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching HR policies..."):
                full_prompt = f"""You are an HR Assistant. Use ONLY the following company HR policy information to answer the question.

{HR_KNOWLEDGE}

Question: {prompt}

Answer concisely and accurately. If the answer is not in the policies, say "Please contact HR directly."
"""
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=full_prompt,
                    )
                    answer = response.text
                except Exception as e:
                    answer = f"⚠️ Error: {e}"

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
