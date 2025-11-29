import streamlit as st
import os
from openai import OpenAI

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

def main():
    st.set_page_config(page_title="HR Assistant Agent", layout="wide")
    st.title("🤖 HR Assistant Agent")
    st.markdown("**Roomans AI Challenge - HR Policy Assistant**")

    # Get OpenAI API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ Add your OPENAI_API_KEY as a Streamlit secret or environment variable!")
        st.info("Go to Settings > Secrets in Streamlit Cloud or set environment variable locally.")
        st.stop()

    client = OpenAI(api_key=api_key)

    # Initialize chat messages state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show HR policies in sidebar
    with st.sidebar:
        st.markdown("### 📋 HR Policies")
        st.code(HR_KNOWLEDGE, language="text")

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask about policies, leave, benefits..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching HR policies..."):
                full_prompt = f"""You are an HR Assistant. Use ONLY the following company HR policy information to answer the question.

{HR_KNOWLEDGE}

Question: {prompt}

Answer concisely and accurately. If the answer is not in the policies, say "Please contact HR directly."
"""
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": full_prompt}]
                    )
                    answer = response.choices[0].message.content
                except Exception as e:
                    answer = f"⚠️ Error: {e}"

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
