"""
app.py — Streamlit UI for CollegeBot
         Run with: python -m streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from rag_chain import load_rag_chain

load_dotenv()

# Support both local .env and Streamlit Cloud secrets
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="CollegeBot — AITM FAQ Assistant",
    page_icon="🎓",
    layout="centered",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Overall background — soft warm white, not cold blue-grey */
    .stApp { background-color: #f5f7ff; }

    /* Sidebar — remove top padding using confirmed data-testid selectors */
    [data-testid="stSidebarContent"] { padding-top: 0 !important; }
    [data-testid="stSidebarHeader"] { padding-top: 0.25rem !important; min-height: unset !important; }

    /* Chat input — confirmed class name from Streamlit 1.35 bundle */
    .stChatInput { background-color: #eef2ff !important; }
    .stChatInput * { background-color: #eef2ff !important; }
    .stChatInput textarea {
        background-color: #eef2ff !important;
        color: #1e1b4b !important;
        caret-color: #3730a3 !important;
    }
    .stChatInput textarea::placeholder { color: #9ca3af !important; }
    /* Floating bar at the bottom of the page */
    [data-testid="stChatInput"] {
        background-color: #eef2ff !important;
    }
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div {
        background-color: #eef2ff !important;
    }

    /* Header — richer indigo gradient */
    .college-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #3730a3 60%, #4f46e5 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 14px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.25);
    }
    .college-header h1 { font-size: 2rem; margin: 0 0 4px 0; }
    .college-header p  { font-size: 0.95rem; margin: 0; opacity: 0.88; }

    /* Chat bubbles */
    .chat-user {
        background: linear-gradient(135deg, #3730a3, #4f46e5);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 10px 16px;
        margin: 6px 0 6px auto;
        max-width: 75%;
        width: fit-content;
        font-size: 0.95rem;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
    }
    .chat-bot {
        background: #ffffff;
        color: #1e1b4b;
        border: 1px solid #e0e7ff;
        border-radius: 18px 18px 18px 4px;
        padding: 10px 16px;
        margin: 6px auto 6px 0;
        max-width: 82%;
        width: fit-content;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.08);
    }
    /* chat-label — dark enough to be visible on #f5f7ff background */
    .chat-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #3730a3;
        margin: 2px 4px;
        letter-spacing: 0.3px;
    }

    /* Suggested questions */
    .stButton > button {
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        color: #3730a3;
        border-radius: 20px;
        font-size: 0.82rem;
        padding: 4px 14px;
        margin: 2px;
    }
    .stButton > button:hover {
        background: #e0e7ff;
        border-color: #4f46e5;
        color: #1e1b4b;
    }

    /* Source expander */
    .source-item {
        background: #eef2ff;
        border-left: 3px solid #4f46e5;
        padding: 8px 12px;
        margin: 6px 0;
        font-size: 0.82rem;
        color: #1e1b4b;
        border-radius: 0 6px 6px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="college-header">
        <h1>🎓 CollegeBot</h1>
        <p>AI-Powered FAQ Assistant — Apex Institute of Technology & Management</p>
        <p style="font-size:0.8rem; margin-top:6px; opacity:0.7;">
            Powered by Qwen 3 · LangChain · FAISS · Built with IBM Bob
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Check for API key ─────────────────────────────────────────────────────────
if not os.environ.get("GROQ_API_KEY"):
    st.error(
        "⚠️ **GROQ_API_KEY not found.**\n\n"
        "1. Get a free key at [console.groq.com](https://console.groq.com)\n"
        "2. Copy `.env.example` → `.env` and paste your key\n"
        "3. Restart the app"
    )
    st.stop()

# ── Load RAG chain (cached across sessions) ───────────────────────────────────
@st.cache_resource(show_spinner="Loading AI model and knowledge base...")
def get_chain():
    return load_rag_chain()

try:
    chain = get_chain()
except FileNotFoundError as e:
    st.error(
        f"⚠️ **Knowledge base not found.**\n\n"
        f"{e}\n\n"
        "Open a terminal in the `collegebot/` folder and run:\n"
        "```bash\npython ingest.py\n```"
    )
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Suggested questions ───────────────────────────────────────────────────────
SUGGESTIONS = [
    "What B.Tech programs are offered?",
    "What is the B.Tech fee structure?",
    "Tell me about hostel facilities",
    "What is the placement record?",
    "How to apply for admission?",
    "What scholarships are available?",
    "What is the attendance requirement?",
    "Which companies recruit from this college?",
]

if not st.session_state.messages:
    st.markdown("**💡 Suggested questions — click to ask:**")
    cols = st.columns(2)
    for i, suggestion in enumerate(SUGGESTIONS):
        if cols[i % 2].button(suggestion, key=f"sug_{i}"):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-label" style="text-align:right;">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-label">🎓 CollegeBot</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bot">{msg["content"]}</div>', unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything about AITM — admissions, fees, hostel, placements...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        result = chain.invoke({"question": user_input})
        answer = result["answer"]
        # Strip Qwen thinking tags if present
        if "<think>" in answer and "</think>" in answer:
            answer = answer[answer.rfind("</think>") + 8:].strip()
        source_docs = result.get("source_documents", [])
        sources = [doc.page_content.strip()[:300] + "..." for doc in source_docs[:3]]

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
    st.rerun()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 CollegeBot")
    st.markdown("**Apex Institute of Technology & Management**")
    st.divider()

    st.markdown("### 📋 Topics I can help with")
    topics = [
        "🎓 B.Tech / M.Tech / MBA Programs",
        "📝 Admission Process & Eligibility",
        "💰 Fee Structure & Scholarships",
        "🏠 Hostel & Mess Facilities",
        "💼 Placement Cell & Companies",
        "📅 Examination System & Results",
        "📚 Library & Infrastructure",
        "📞 Contact & Administration",
    ]
    for topic in topics:
        st.markdown(f"- {topic}")

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        chain.memory.clear()
        st.rerun()

    st.divider()
    st.markdown(
        "<small style='color:#6b7280;'>Built using IBM Bob · LangChain · "
        "Groq Qwen3 · FAISS · Streamlit</small>",
        unsafe_allow_html=True,
    )

# ── Late-injected overrides (runs after Streamlit renders its own styles) ────
st.markdown("""
<style>
/* ── SIDEBAR: hide the stSidebarHeader (it's the empty gap area) ── */
[data-testid="stSidebarHeader"] {
    display: none !important;
}

/* ── CHAT INPUT: exact class from DevTools ── */
.st-emotion-cache-vj1c9o {
    background-color: #eef2ff !important;
    border: 1px solid #c7d2fe !important;
    border-radius: 12px !important;
}
.st-emotion-cache-vj1c9o textarea {
    background-color: #eef2ff !important;
    color: #1e1b4b !important;
    caret-color: #3730a3 !important;
}
.st-emotion-cache-vj1c9o textarea::placeholder {
    color: #9ca3af !important;
}
/* parent container (ea3mdgi6) and its wrapper */
.ea3mdgi6 {
    background-color: #eef2ff !important;
}
.stBottom, .stBottom > div {
    background-color: #f5f7ff !important;
}
[data-testid="stBottomBlockContainer"] {
    background-color: #f5f7ff !important;
}
[data-testid="stBottomBlockContainer"] > div {
    background-color: #f5f7ff !important;
}
</style>
""", unsafe_allow_html=True)
