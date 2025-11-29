import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import CharacterTextSplitter
import pinecone
from hr_policies import policies

load_dotenv()

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment=os.getenv('PINECONE_ENVIRONMENT')
)

index_name = 'hr-assistant-policies'
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, dimension=1536, metric='cosine')

# New imports for LangChain v0.3+
embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.create_documents(policies)

vectorstore = PineconeVectorStore.from_documents(
    texts, embeddings, index_name=index_name
)
print("✅ HR policies indexed successfully!")
