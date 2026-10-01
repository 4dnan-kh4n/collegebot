"""
rag_chain.py — Build the LangChain RAG pipeline using:
               - FAISS vector store (local)
               - HuggingFace embeddings
               - Groq LLaMA3 as the LLM
"""

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

load_dotenv()

FAISS_INDEX_PATH = "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SYSTEM_PROMPT = """You are CollegeBot, a friendly and helpful AI assistant exclusively for \
Apex Institute of Technology & Management (AITM), an Indian engineering college.

IMPORTANT RULES:
1. You ONLY answer questions related to AITM college — admissions, fees, hostel, placements, \
exams, scholarships, programs, infrastructure, and campus life.
2. If the student asks anything UNRELATED to the college (e.g. weather, sports, news, general \
knowledge, coding help, jokes, politics, etc.), respond with EXACTLY this message:
   "I'm CollegeBot, your AITM college assistant! I can only help with college-related topics \
such as admissions, fees, hostel, placements, exams, and campus life. For your question, \
please try a general search engine. Is there anything about AITM I can help you with?"
3. Use ONLY the context provided below to answer college-related questions.
4. If a college question is not covered in the context, say:
   "I don't have that specific information right now. Please contact the admissions office \
at admissions@aitm.edu.in or call +91-80-12345678 for accurate details."
5. Always be warm, friendly, and concise. Use simple language suitable for students.

Context:
{context}

Chat History:
{chat_history}

Student Question: {question}
CollegeBot Answer:"""

PROMPT = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=SYSTEM_PROMPT,
)


def load_rag_chain():
    """Load the FAISS index and build the RAG chain. Returns the chain."""
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(
            f"FAISS index not found at '{FAISS_INDEX_PATH}/'. "
            "Please run: python ingest.py"
        )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )

    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    llm = ChatGroq(
        model="qwen/qwen3.8-27b",
        temperature=0.3,
        api_key=os.environ["GROQ_API_KEY"],
    )

    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=5,  # keep last 5 turns in memory
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT},
        return_source_documents=True,
        verbose=False,
    )

    return chain
