# 🎓 CollegeBot — AI-Powered College FAQ Chatbot

> **IBM SkillBuild ML & Applied AI Internship Project**  
> Built using **IBM Bob** · **LangChain** · **Groq LLaMA3** · **FAISS** · **Streamlit**

---

## 📌 Project Overview

CollegeBot is a Retrieval-Augmented Generation (RAG) based AI chatbot that answers frequently asked questions about an Indian engineering college. It uses a local FAISS vector store to retrieve relevant FAQ passages and passes them to the LLaMA 3 LLM (via Groq's free API) to generate accurate, context-grounded answers.

### 🔑 Key Features
- 💬 Natural language Q&A about college topics
- 🔍 Semantic search using FAISS + HuggingFace embeddings
- 🧠 Conversation memory (remembers last 5 turns)
- 📚 Source passage display for every answer
- 🎨 Clean, professional Streamlit UI
- ⚡ Fast responses via Groq's LLaMA 3 (8B) model

---

## 🏗️ Architecture

```
User Question
     │
     ▼
[Streamlit UI]  ──►  [LangChain ConversationalRetrievalChain]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    [FAISS Vector Store]            [Groq LLaMA3 LLM]
    (semantic retrieval)           (answer generation)
              │
              ▼
    [HuggingFace Embeddings]
    all-MiniLM-L6-v2
```

---

## 📁 Project Structure

```
collegebot/
├── app.py                  ← Streamlit UI + chat logic
├── ingest.py               ← Build FAISS index from FAQ data
├── rag_chain.py            ← LangChain RAG pipeline
├── requirements.txt        ← Python dependencies
├── .env.example            ← Environment variable template
├── data/
│   └── college_faq.txt     ← Knowledge base (FAQ document)
└── faiss_index/            ← Auto-created by ingest.py
    ├── index.faiss
    └── index.pkl
```

---

## ⚙️ Setup & Installation

### Step 1 — Prerequisites
Make sure you have **Python 3.9+** installed.

```bash
python --version
```

### Step 2 — Install Dependencies

```bash
cd collegebot
pip install -r requirements.txt
```

### Step 3 — Get a Free Groq API Key
1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → Create a new key
4. Copy the key

### Step 4 — Configure Environment

```bash
# Copy the example file
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux

# Open .env and paste your Groq API key
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 5 — Build the Knowledge Base (Run Once)

```bash
python ingest.py
```

You will see output like:
```
📄 Loading FAQ document...
✂️  Splitting into chunks...
   → 87 chunks created
🔢 Generating embeddings (this may take a minute)...
💾 Building and saving FAISS index...
✅ FAISS index saved to 'faiss_index/'
```

### Step 6 — Launch the App

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🚀

---

## 💡 Example Questions to Try

| Category | Sample Question |
|---|---|
| Admissions | "What is the eligibility for B.Tech admission?" |
| Fees | "What is the fee for B.Tech CSE?" |
| Scholarships | "What scholarships are available for SC/ST students?" |
| Hostel | "What are the hostel charges and facilities?" |
| Placement | "What is the average placement package?" |
| Exams | "What is the minimum attendance required?" |
| Programs | "What M.Tech programs does the college offer?" |
| Contact | "How do I contact the admissions office?" |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq API — LLaMA 3.1 8B Instant (free tier) |
| Orchestration | LangChain `ConversationalRetrievalChain` |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS (local, CPU) |
| Memory | `ConversationBufferWindowMemory` (k=5) |
| UI | Streamlit |
| AI Coding Tool | IBM Bob |

---

## 🔧 Customization

### Add More FAQ Content
Edit `data/college_faq.txt` and add more Q&A pairs, then re-run:
```bash
python ingest.py
```

### Switch to a Different LLM Model
In `rag_chain.py`, change the model name:
```python
llm = ChatGroq(model="llama3-70b-8192", ...)  # larger model
llm = ChatGroq(model="mixtral-8x7b-32768", ...)  # Mixtral
```

### Use a PDF Instead of TXT
In `ingest.py`, replace `TextLoader` with:
```python
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("data/college_brochure.pdf")
```

---

## 📊 How RAG Works

1. **Ingestion** (`ingest.py`): The FAQ document is split into small chunks, each chunk is converted into a numerical vector (embedding) and stored in a FAISS index.

2. **Retrieval** (`rag_chain.py`): When a user asks a question, the question is embedded and the top-4 most similar FAQ chunks are retrieved from FAISS.

3. **Augmentation**: The retrieved chunks are injected into a prompt template as "context".

4. **Generation**: The Groq LLaMA3 model reads the context + question and generates a grounded answer.

---

## 🙏 Acknowledgements

- **IBM SkillBuild** — ML & Applied AI Internship Program
- **IBM Bob** — AI coding assistant used to build this project
- **Groq** — Free LLM API with LLaMA3
- **LangChain** — RAG orchestration framework
- **Meta AI** — LLaMA 3 open-source model

---

*Built as part of the IBM SkillBuild Machine Learning & Applied AI Internship Program.*
