# HR Assistant Agent

## Overview
AI agent that answers employee queries about HR policies and leave benefits using Retrieval Augmented Generation (RAG).

## Features
- Answers policy questions accurately
- Sources responses from company HR documents
- Conversational chat interface

## Tech Stack
- LangChain (RAG pipeline)
- OpenAI GPT (LLM + Embeddings)
- Pinecone (Vector Database)
- Streamlit (UI)

## Setup
1. Copy `.env` template and add your API keys
2. `pip install -r requirements.txt`
3. `python ingest_data.py` (first time only)
4. `streamlit run hr_agent.py`

## Demo
[Live Demo Link - Deployed on Streamlit Cloud]



