import streamlit as st
import os
from openai import OpenAI
import streamlit as st

# HR Knowledge Base
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
    
    # OpenAI API Key from Streamlit Secrets
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ Add OPENAI_API_KEY in Streamlit Cloud Secrets!")
        st.info("Settings → Secrets → Add `OPENAI_API_KEY`")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar with policies
    with st.sidebar:
        st.markdown("### 📋 HR Policies")
        st.code(HR_KNOWLEDGE, language="text")
    
    # Show chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about policies, leave, benefits..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Searching HR policies..."):
                full_prompt = f"""You are an HR Assistant. Answer using ONLY this company policy information:

{HR_KNOWLEDGE}

Question: {prompt}

Answer concisely and accurately. If not in policies, say "Please contact HR directly.""""
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": full_prompt}]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
