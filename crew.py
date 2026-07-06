"""
crew.py
--------
Assembles the CrewAI crew and runs the full multi-agent legal pipeline.
"""

import os
from dotenv import load_dotenv
from crewai import Crew, Process

from agents import (
    build_case_intake_agent,
    build_ipc_section_agent,
    build_legal_precedent_agent,
    build_drafting_agent,
)
from tasks import (
    build_case_intake_task,
    build_ipc_section_task,
    build_precedent_task,
    build_drafting_task,
)

load_dotenv()

# Configure Groq as an OpenAI-compatible provider
os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY", "sk-dummy-key")


def run_legal_crew(user_query: str) -> dict:
    """
    Orchestrate all four agents sequentially for the given legal query.

    Returns a dict with:
        - 'final_output': the complete legal advisory document (string)
        - 'tasks_outputs': list of individual agent outputs (strings)
    """

    # ── Build agents ──────────────────────────────────────────────────────
    intake_agent = build_case_intake_agent()
    ipc_agent = build_ipc_section_agent()
    precedent_agent = build_legal_precedent_agent()
    drafting_agent = build_drafting_agent()

    # ── Build tasks (sequential — each depends on previous) ───────────────
    intake_task = build_case_intake_task(intake_agent, user_query)
    ipc_task = build_ipc_section_task(ipc_agent, context_tasks=[intake_task])
    precedent_task = build_precedent_task(precedent_agent, context_tasks=[intake_task, ipc_task])
    drafting_task = build_drafting_task(
        drafting_agent,
        context_tasks=[intake_task, ipc_task, precedent_task],
    )

    # ── Assemble crew ─────────────────────────────────────────────────────
    crew = Crew(
        agents=[intake_agent, ipc_agent, precedent_agent, drafting_agent],
        tasks=[intake_task, ipc_task, precedent_task, drafting_task],
        process=Process.sequential,     # tasks run one after another in order
        verbose=True,
        memory=False,                   # set True to enable long-term crew memory
        max_rpm=10,                     # rate limit: requests per minute to LLM
    )

    # ── Kick off the crew ─────────────────────────────────────────────────
    result = crew.kickoff()

    # Collect individual task outputs
    tasks_outputs = []
    for task in [intake_task, ipc_task, precedent_task, drafting_task]:
        if hasattr(task, "output") and task.output:
            tasks_outputs.append(
                {
                    "agent": task.agent.role,
                    "output": str(task.output),
                }
            )

    return {
        "final_output": str(result),
        "tasks_outputs": tasks_outputs,
    }


# ─────────────────────────────────────────────────────────────────────────────
#
#  💡 NOVEL RESEARCH EXTENSION — "LexGraph"
#  For Conference Paper Publication
#
#  Title: "LexGraph: A Confidence-Calibrated, Jurisdiction-Aware Multi-Agent
#          RAG System with Citation Graph Generation for Legal AI Assistants"
#
#  Core Novel Contributions:
#
#  1. JURISDICTION-AWARE ROUTING
#     Add a pre-processing agent (Jurisdiction Classifier) that detects the
#     relevant jurisdiction (Central IPC, State amendments, IT Act, POCSO, etc.)
#     and dynamically routes queries to the correct legal corpus. This adds a
#     metadata-aware RAG layer — a significant novelty over flat IPC search.
#
#  2. CONFIDENCE SCORE CALIBRATION
#     After each agent produces output, a Confidence Calibration Agent scores
#     each identified IPC section and precedent on a 0-1 scale using:
#       - Semantic similarity to the query (cosine from ChromaDB)
#       - LLM self-assessment (chain-of-thought confidence elicitation)
#       - Cross-agent agreement (do multiple agents identify the same section?)
#     Outputs are tagged with confidence bands: HIGH / MEDIUM / LOW.
#     This directly addresses the hallucination problem identified in the
#     literature review (Magesh et al., 2024 — 17-33% hallucination rate).
#
#  3. LEGAL CITATION GRAPH
#     Build a directed graph (NetworkX) where nodes are legal sections/cases
#     and edges represent "cited-by" or "overruled-by" relationships.
#     This graph is used to:
#       a) Identify whether a precedent is still good law.
#       b) Find additional related sections automatically.
#       c) Visualise the legal reasoning chain as a DAG.
#     Novelty: No existing legal RAG system generates citation graphs
#     dynamically from retrieved precedents.
#
#  4. TEMPORAL LAW TRACKING
#     Attach a "valid_from" / "valid_to" timestamp to each IPC section
#     (important because IPC is being replaced by BNS — Bharatiya Nyaya Sanhita
#     from July 2024). The system automatically flags deprecated sections and
#     maps them to their BNS equivalents. This is highly timely and publishable.
#
#  5. MULTILINGUAL OUTPUT
#     Add a post-processing translation agent (using Google Translate API or
#     IndicTrans2) that can render the final legal document in Hindi, Tamil,
#     Marathi, Bengali, etc. — addressing access to justice in rural India
#     (directly referenced in the PDF introduction).
#
#  EVALUATION METRICS (Novel Contribution):
#     - LexHallu Score: % of cited sections that actually apply to the case
#       (human-annotated gold standard on 200 test cases)
#     - PrecedentRecall@K: proportion of relevant landmark cases retrieved
#     - DocumentCoherence: BERTScore of final draft vs. human-drafted document
#     - JurisdictionAccuracy: % of cases correctly classified by jurisdiction
#
#  This combination of contributions (jurisdiction-aware RAG + confidence
#  calibration + citation graphs + BNS transition awareness + multilingual)
#  is novel enough for IEEE ICTAI, ACL Findings, or JURIX conference.
#
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    # Quick CLI test
    test_query = (
        "My neighbour physically assaulted me yesterday, causing bruises on my "
        "face and arms. He also threatened to kill me if I reported to the police. "
        "I have two witnesses who saw the incident."
    )
    result = run_legal_crew(test_query)
    print("\n" + "=" * 80)
    print("FINAL LEGAL DOCUMENT")
    print("=" * 80)
    print(result["final_output"])
