# ⚖️ Multi-Agent AI Legal Assistant (CrewAI + RAG)

An AI-powered legal assistance system that uses a **multi-agent architecture** and **Retrieval-Augmented Generation (RAG)** to analyze legal queries, retrieve relevant Indian legal provisions, research legal precedents, and generate structured legal analysis.

The system uses specialized AI agents coordinated through CrewAI, with Groq-hosted LLM inference and an interactive Streamlit interface.

> **Disclaimer:** This project is intended for educational and demonstration purposes only. The generated responses do not constitute professional legal advice and should not replace consultation with a qualified legal professional.

---

## 🚀 Features

* 🤖 Multi-agent legal analysis workflow using CrewAI
* 📋 Case intake and structured issue identification
* 📚 Retrieval of relevant Indian legal provisions
* ⚖️ Legal precedent research
* 🧠 LLM-powered legal reasoning and analysis
* 🔎 Retrieval-Augmented Generation (RAG)
* 🗃️ ChromaDB-based vector storage
* 🌐 Web-assisted legal research
* 📝 Structured legal report generation
* 💾 Downloadable analysis reports
* 🖥️ Interactive Streamlit user interface
* 🔐 Secure API key management through environment variables

---

## 🧠 Multi-Agent Architecture

The application decomposes legal analysis into specialized tasks handled by dedicated agents.

### 1. Case Intake Agent

Analyzes the user's legal query and converts the unstructured description into a structured case brief.

Responsibilities include:

* Identifying the core facts
* Determining the parties involved
* Extracting important events
* Identifying potential legal issues
* Preparing structured context for downstream agents

### 2. Legal Research Agent

Retrieves relevant legal provisions based on the facts and legal issues identified during case intake.

Responsibilities include:

* Searching the legal knowledge base
* Identifying potentially applicable provisions
* Providing relevant legal context for further analysis

### 3. Legal Precedent Research Agent

Researches relevant judicial precedents and supporting legal information.

Responsibilities include:

* Searching for related legal cases
* Finding potentially relevant judicial decisions
* Providing precedent context for the final analysis

### 4. Legal Document Drafting Agent

Combines the case analysis, retrieved legal provisions, and precedent research into a structured final report.

Responsibilities include:

* Synthesizing outputs from previous agents
* Explaining relevant legal issues
* Organizing applicable legal provisions
* Summarizing precedent information
* Suggesting possible next steps
* Producing a readable legal analysis report

---

## 🔄 Workflow

```text
User Legal Query
        │
        ▼
┌──────────────────────┐
│   Streamlit Web UI   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Case Intake Agent  │
│  Facts & Legal Issues│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────┐
│   Legal Research Agent   │
│ Legal Provision Retrieval│
└──────────┬───────────────┘
           │
           ▼
┌───────────────────────────┐
│ Precedent Research Agent  │
│ Case Law & Web Research   │
└──────────┬────────────────┘
           │
           ▼
┌──────────────────────────┐
│ Legal Drafting Agent     │
│ Final Structured Report  │
└──────────┬───────────────┘
           │
           ▼
  Legal Analysis Report
           │
           ▼
     Download as TXT
```

---

## 🛠️ Technology Stack

| Technology            | Purpose                                           |
| --------------------- | ------------------------------------------------- |
| Python                | Core application development                      |
| CrewAI                | Multi-agent orchestration                         |
| Groq                  | LLM inference                                     |
| Llama 3.3 70B         | Language model for agent reasoning and generation |
| RAG                   | Retrieval-grounded response generation            |
| ChromaDB              | Vector database and retrieval                     |
| Sentence Transformers | Local text embeddings                             |
| DuckDuckGo Search     | Web-assisted legal research                       |
| Streamlit             | Interactive web application                       |

---

## 📁 Project Structure

```text
Multi-Agent-AI-Legal-Assistant/
│
├── data/
│   └── ipc_sections.py
│
├── tools/
│   ├── ipc_search_tool.py
│   └── legal_precedent_tool.py
│
├── agents.py
├── app.py
├── crew.py
├── tasks.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Main Components

* `app.py` — Streamlit user interface and application entry point
* `agents.py` — Definitions of specialized legal AI agents
* `tasks.py` — Task definitions and expected outputs
* `crew.py` — Multi-agent workflow orchestration
* `data/` — Legal knowledge resources used by the application
* `tools/` — Custom legal provision and precedent research tools

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Multi-Agent-AI-Legal-Assistant
```

### 2. Create a virtual environment

For Windows:

```bash
py -3.11 -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Alternatively, copy `.env.example` and replace the placeholder API key with your own key.

### 5. Run the application

```bash
streamlit run app.py
```

The application will start locally and can be accessed through the URL displayed in the terminal.

---

## 💡 Example Query

```text
A friend of mine discovered that someone had gained unauthorized access to their social media account, changed the password, and used the account to send fraudulent messages to their contacts.

What legal action can my friend take under Indian law? Please identify the relevant legal provisions, applicable legal precedents, and recommended next steps.
```

The system processes the query through the multi-agent workflow and generates a structured legal analysis report.

---

## 📸 Application Preview

Screenshots of the application interface and generated legal analysis will be added here.

```text
screenshots/
├── home-page.png
├── query-input.png
└── generated-analysis.png
```

---

## 📄 Sample Output

A sample generated legal analysis report will be available in:

```text
sample_outputs/
└── cybercrime_case_analysis.txt
```

This demonstrates the complete workflow from user query to structured legal analysis.

---

## 🔮 Future Improvements

* Expand the legal knowledge base
* Add support for more Indian statutes and legal domains
* Improve citation traceability for retrieved provisions and precedents
* Add PDF document upload and analysis
* Add conversational follow-up questions
* Introduce source verification and confidence scoring
* Add multilingual support for Indian languages
* Improve retrieval evaluation and response quality testing
* Deploy the application for public demonstration

---

## ⚠️ Limitations

* AI-generated legal analysis may contain errors or incomplete interpretations.
* Retrieved legal information should be independently verified.
* Web search results may vary depending on source availability.
* The application is a prototype intended for educational and research purposes.
* The system should not be used as a substitute for professional legal advice.

---

## 👨‍💻 Author

**Shreyas Karanjkar**

Developed as a project exploring **Multi-Agent Systems, Retrieval-Augmented Generation, LLM applications, and Legal AI**.
