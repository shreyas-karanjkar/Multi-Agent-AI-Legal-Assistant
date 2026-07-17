"""
app.py
-------
Streamlit frontend.
LLM: Groq
Search: DuckDuckGo
Vector DB: ChromaDB local
Embeddings: sentence-transformers local
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()

# Configure Groq as an OpenAI-compatible provider
# Note: OPENAI_BASE_URL is for v1.0+, OPENAI_API_BASE is for older versions.
os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY", "sk-dummy-key")

import streamlit as st

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚖️ AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Theme-aware variables for custom components */
    :root {
        --doc-bg: #ffffff;
        --doc-text: #1a1a1a;
        --doc-border: #dee2e6;
        --disclaimer-bg: #fff3cd;
        --disclaimer-border: #ffc107;
        --disclaimer-text: #856404;
    }

    [data-theme="dark"] {
        --doc-bg: #1e1e1e;
        --doc-text: #fafafa;
        --doc-border: #333333;
        --disclaimer-bg: #2a2300;
        --disclaimer-border: #ffc107;
        --disclaimer-text: #ffe082;
    }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem; border-radius: 12px; margin-bottom: 2rem;
        text-align: center; color: white;
    }
    .main-header h1 { font-size: 2.5rem; margin: 0; color: white !important; }
    .main-header p  { font-size: 1.05rem; opacity: 0.85; margin-top: 0.4rem; color: white !important; }
    
    .stack-row {
        display: flex; gap: 8px; flex-wrap: wrap; margin: 0.5rem 0;
    }
    .stack-pill {
        background: rgba(46, 125, 50, 0.1); color: #2e7d32;
        border: 1px solid rgba(46, 125, 50, 0.3); border-radius: 20px;
        padding: 3px 12px; font-size: 0.78rem; font-weight: 500;
    }
    .final-doc {
        background-color: var(--doc-bg); 
        border: 1px solid var(--doc-border);
        color: var(--doc-text) !important;
        border-radius: 12px; padding: 2.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        line-height: 1.8;
        margin-top: 1.5rem;
        font-size: 1.05rem;
    }
    .disclaimer {
        background-color: var(--disclaimer-bg); 
        border: 1px solid var(--disclaimer-border);
        color: var(--disclaimer-text);
        border-radius: 8px; padding: 1rem; font-size: 0.85rem;
        margin-top: 1.5rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit status widget */
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <h1>⚖️ Multi-Agent AI Legal Assistant</h1>
        <p>Multi-Agent RAG · CrewAI · IPC Sections · Legal Precedents</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="stack-row">
        <span class="stack-pill">🧠 Groq LLM</span>
        <span class="stack-pill">🦙 Llama 3.3 70B</span>
        <span class="stack-pill">🗄️ ChromaDB Local</span>
        <span class="stack-pill">🔍 DuckDuckGo Search</span>
        <span class="stack-pill">📐 Sentence Transformers</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <style>
        /* Modern Native Adaptive Styling */
        :root {
            /* These will adapt based on Streamlit's native theme */
            --doc-bg: inherit;
            --doc-text: inherit;
            --doc-border: #444444;       
        }
        
        .main-header {
            padding: 2.5rem;
            border-radius: 12px;
            text-align: center;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            margin-bottom: 2rem;
            color: white !important;
        }
        .main-header p, .main-header h1 {
            color: white !important;
        }
        .stack-pill {
            background-color: rgba(46, 125, 50, 0.1);
            color: #2e7d32;
            border: 1px solid rgba(46, 125, 50, 0.4);
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            display: inline-block;
            margin: 0 5px;
            font-weight: 500;
        }
        /* Dark mode adaptation for stack-pill is handled by standard transparency */
        @media (prefers-color-scheme: dark) {
            .stack-pill {
                background-color: rgba(165, 214, 167, 0.1);
                color: #a5d6a7;
                border-color: rgba(165, 214, 167, 0.3);
            }
        }
        .final-doc {
            background-color: var(--doc-bg);
            color: var(--doc-text);
            border: 1px solid var(--doc-border);
            border-radius: 10px;
            padding: 30px;
            margin-top: 20px;
            font-family: 'Georgia', serif;
            line-height: 1.8;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.02);
        }
        .disclaimer {
            background-color: rgba(255, 193, 7, 0.1);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 0.9em;
            border-left: 5px solid #ffc107;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.info("💡 **Tip:** Use the top-right menu (`⋮`) -> **Settings** -> **Theme** to switch between Light and Dark mode flawlessly.", icon="ℹ️")

    # Restored model choice selection
    st.markdown("---")
    st.subheader("🤖 Model Settings")
    model_choice = st.selectbox(
        "Choose Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
        index=0,
        help="Llama 3.3 70B is more accurate. 8B & Gemma are faster but simpler."
    )
    os.environ["GROQ_MODEL"] = model_choice


# ── Key Status ────────────────────────────────────────────────────────────────
groq_configured = bool(os.getenv("GROQ_API_KEY"))

if not groq_configured:
    st.warning(
        "⚠️ **Groq API key not set.** Please ensure it is configured in the environment.",
        icon="🔑",
    )
else:
    st.success(
        f"✅ System Ready · Model: `{os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')}`",
        icon="🟢",
    )

# ── Example Queries ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📝 Describe Your Legal Problem")

example_queries = {
    "Select an example...": "",
    "🤜 Assault & Threat": (
        "My neighbour physically assaulted me yesterday causing visible bruises on my face. "
        "He also threatened to kill me if I report to the police. I have two witnesses."
    ),
    "💑 Domestic Violence / 498A": (
        "My husband and his family have been harassing me for two years demanding additional dowry. "
        "Last week my husband hit me. I have medical reports of my injuries. "
        "What are my legal options under Section 498A IPC?"
    ),
    "💻 Cyber Fraud / Section 420": (
        "I received a call from someone claiming to be a bank official. "
        "They convinced me to share my OTP and Rs 85,000 was transferred without my consent. "
        "I have the call recording and transaction history."
    ),
    "🏘️ Property Trespass": (
        "My landlord forcibly entered my rented premises and changed the locks while I was away, "
        "throwing out all my belongings. I have a valid rental agreement signed 8 months ago."
    ),
    "📱 Online Stalking / 354D": (
        "An ex-colleague keeps following me, sending threatening messages on WhatsApp, "
        "and posting defamatory content about me on social media. "
        "I have screenshots of all messages."
    ),
    "🔒 Theft / Section 379": (
        "My laptop and phone were stolen from my office desk while I was away for lunch. "
        "The office has CCTV cameras and I suspect a colleague. "
        "What should I do and under which IPC section can I file a complaint?"
    ),
}

selected_example = st.selectbox("Quick examples:", list(example_queries.keys()))

user_query = st.text_area(
    "Your Legal Problem",
    value=example_queries[selected_example],
    height=160,
    placeholder=(
        "Describe your legal issue in detail. Include:\n"
        "• What happened (incident, date, location)\n"
        "• Who is involved (you, the accused, witnesses)\n"
        "• Evidence you have (receipts, messages, medical reports, CCTV)\n"
        "• What outcome you want (FIR, legal notice, compensation)"
    ),
)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_btn = st.button(
        "⚖️ Analyse My Case",
        type="primary",
        use_container_width=True,
        disabled=not groq_configured or not user_query.strip(),
    )

if not groq_configured:
    st.caption("⚠️ API key missing in environment.")

# ── State Initialization ──────────────────────────────────────────────────────
if "legal_result" not in st.session_state:
    st.session_state.legal_result = None
if "run_trigger" not in st.session_state:
    st.session_state.run_trigger = False
if "current_query" not in st.session_state:
    st.session_state.current_query = ""
if "pipeline_error" not in st.session_state:
    st.session_state.pipeline_error = None

# ── Main Processing ───────────────────────────────────────────────────────────
# ── Main Processing Logic ─────────────────────────────────────────────────────

# Register button click
if run_btn:
    st.session_state.run_trigger = True
    st.session_state.current_query = user_query
    st.session_state.legal_result = None  # Clear previous result
    st.session_state.pipeline_error = None

# If we have a trigger to run, execute the pipeline
if st.session_state.run_trigger:
    from crew import run_legal_crew
    st.divider()
    st.markdown("## 🔄 Live Agent Pipeline")

    step1 = st.expander("🔍 Step 1 · Case Intake Agent", expanded=True)
    step2 = st.expander("📖 Step 2 · IPC Section Agent (ChromaDB RAG)", expanded=False)
    step3 = st.expander("⚖️ Step 3 · Legal Precedent Agent (DuckDuckGo)", expanded=False)
    step4 = st.expander("📝 Step 4 · Legal Document Drafting Agent", expanded=False)

    step1.info("⏳ Analysing case details...")
    step2.info("⏳ Waiting for intake...")
    step3.info("⏳ Waiting for IPC analysis...")
    step4.info("⏳ Waiting for precedents...")

    prog = st.progress(10, text="Agents initialising... (This process takes up to 2 minutes. Please do not navigate away)")

    with st.spinner("🤖 CrewAI Agents are actively processing the legal pipeline..."):
        try:
            result = run_legal_crew(st.session_state.current_query)
            st.session_state.legal_result = result
            prog.progress(100, text="✅ Done!")
        except Exception as e:
            st.session_state.pipeline_error = str(e)
            prog.progress(0)
    
    # After finishing or erroring out, turn off the trigger so we don't re-run
    st.session_state.run_trigger = False

# ── Result Display Logic ──────────────────────────────────────────────────────

if st.session_state.pipeline_error:
    st.divider()
    st.error(f"❌ Error: {st.session_state.pipeline_error}")
    st.warning("🔄 **Groq rate limit hit.** Free tier handles ~6000 tokens/min.\n\n"
               "**Fix options:**\n"
               "1. Wait 60 seconds and try again\n"
               "2. Switch to `llama-3.1-8b-instant` in the sidebar (Higher limits)\n"
               "3. Ensure your query format is standard.")

if st.session_state.legal_result:
    result_container = st.session_state.legal_result
    tasks_outputs = result_container.get("tasks_outputs", [])
    final_output  = result_container.get("final_output", "")

    st.divider()
    st.markdown("## 📊 Analysis Pipeline Results")

    labels = [
        "🔍 Step 1 · Case Intake Agent",
        "📖 Step 2 · IPC Section Agent (ChromaDB RAG)",
        "⚖️ Step 3 · Legal Precedent Agent (DuckDuckGo)",
        "📝 Step 4 · Legal Document Drafting Agent",
    ]
    
    for i, label in enumerate(labels):
        with st.expander(label, expanded=(i == 3)):
            if i < len(tasks_outputs):
                st.success(f"✅ {tasks_outputs[i]['agent']} completed")
                st.markdown(tasks_outputs[i]["output"])
            else:
                st.info("Included in the final document below.")

    # ── Final Document ────────────────────────────────────────────────────────
    st.divider()
    st.markdown("## 📄 Final Legal Advisory Document")

    formatted = final_output.replace("\n", "<br>")
    st.markdown(f'<div class="final-doc">{formatted}</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "📥 Download .txt",
            data=final_output,
            file_name="legal_advisory.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_b:
        st.download_button(
            "📋 Download .md",
            data=final_output,
            file_name="legal_advisory.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown(
        '<div class="disclaimer">'
        "⚠️ <strong>Disclaimer:</strong> This document is AI-generated for informational "
        "purposes only. It does not constitute legal advice. Always consult a qualified "
        "licensed advocate before taking legal action."
        "</div>",
        unsafe_allow_html=True,
    )
