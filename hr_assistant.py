import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# HR Knowledge Base (Directly in code - NO external files!)
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

@st.cache_resource
def get_llm():
    return ChatOpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        model="gpt-4o-mini",
        temperature=0.1
    )

def main():
    st.set_page_config(page_title="HR Assistant Agent", layout="wide")
    st.title("🤖 HR Assistant Agent")
    st.markdown("**AI-powered HR policy assistant for Roomans AI Challenge**")
    
    # Check API key
    if not os.getenv('OPENAI_API_KEY'):
        st.error("❌ Add `OPENAI_API_KEY` to `.env` file!")
        st.code("OPENAI_API_KEY=sk-your-key-here")
        return
    
    llm = get_llm()
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Instructions
    st.sidebar.markdown("### 📋 HR Policies")
    st.sidebar.code(HR_KNOWLEDGE, language="text")
    
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
            with st.spinner("Answering..."):
                full_prompt = f"""
                You are an HR Assistant. Answer using ONLY this company policy information:
                
                {HR_KNOWLEDGE}
                
                Question: {prompt}
                
                Answer concisely and accurately. If not in policies, say "Please contact HR directly."
                """
                
                response = llm.invoke(full_prompt)
                st.markdown(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})

if __name__ == "__main__":
    main()
