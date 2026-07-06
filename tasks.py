"""
tasks.py
---------
Defines the four sequential tasks for the AI Legal Assistant CrewAI pipeline.
Each task corresponds to one agent and feeds its output to the next.
"""

from crewai import Task
from crewai import Agent


def build_case_intake_task(agent: Agent, user_query: str) -> Task:
    return Task(
        description=(
            f"A user has presented the following legal problem:\n\n"
            f"'''\n{user_query}\n'''\n\n"
            "Your task is to:\n"
            "1. Read the user's description carefully.\n"
            "2. Identify and list ALL key facts (who, what, when, where, how).\n"
            "3. Identify the parties involved (complainant, accused, witnesses, etc.).\n"
            "4. Classify the matter: Civil or Criminal? Explain why.\n"
            "5. Identify the nature of the offence(s) involved in plain language.\n"
            "6. Provide a structured case summary (max 300 words) that the next agent "
            "can use to find applicable IPC sections.\n"
            "7. Note any urgency or immediate legal remedies the user might need "
            "(e.g., police complaint, restraining order)."
        ),
        expected_output=(
            "A structured case intake report in the following format:\n"
            "## Case Intake Report\n"
            "**Case Type:** (Civil / Criminal / Mixed)\n"
            "**Parties Involved:** ...\n"
            "**Key Facts:** (numbered list)\n"
            "**Nature of Offence(s):** ...\n"
            "**Urgency / Immediate Actions:** ...\n"
            "**Case Summary for Legal Analysis:** (concise paragraph)"
        ),
        agent=agent,
    )


def build_ipc_section_task(agent: Agent, context_tasks: list) -> Task:
    return Task(
        description=(
            "Based on the structured case intake report from the previous step, "
            "use the IPC Section Search Tool to identify ALL applicable IPC sections.\n\n"
            "Your task is to:\n"
            "1. Use the IPC Section Search Tool with the case summary as the query.\n"
            "2. Identify the top 3-7 most applicable IPC sections.\n"
            "3. For EACH section, explain:\n"
            "   a. The section number and title.\n"
            "   b. WHY this section applies to the specific facts of this case.\n"
            "   c. The punishment the accused may face under this section.\n"
            "4. Distinguish between primary sections (directly applicable) and "
            "secondary/supporting sections.\n"
            "5. Note whether any sections are non-bailable, cognizable, or "
            "triable by which court."
        ),
        expected_output=(
            "A detailed IPC Sections Report in the following format:\n"
            "## Applicable IPC Sections\n"
            "### Primary Sections\n"
            "(For each: Section No. | Title | Why It Applies | Punishment | "
            "Cognizable/Non-cognizable | Bailable/Non-bailable)\n"
            "### Supporting Sections\n"
            "(Same format)\n"
            "### Summary Table\n"
            "(Section | Title | Max Punishment)"
        ),
        agent=agent,
        context=context_tasks,
    )


def build_precedent_task(agent: Agent, context_tasks: list) -> Task:
    return Task(
        description=(
            "Based on the case facts and the identified IPC sections, search for "
            "relevant legal precedents — landmark judgments from the Supreme Court "
            "and High Courts of India that are applicable to this case.\n\n"
            "Your task is to:\n"
            "1. Use the Legal Precedent Search Tool with specific queries combining "
            "the case type, IPC sections, and key facts.\n"
            "2. Find 3-6 highly relevant precedent cases.\n"
            "3. For EACH precedent, provide:\n"
            "   a. Case name and citation (court + year).\n"
            "   b. Brief facts of the case.\n"
            "   c. Key holding / ratio decidendi.\n"
            "   d. How it applies to the current case.\n"
            "4. Identify if any precedent is particularly helpful for the defence "
            "or prosecution.\n"
            "5. Mention the evidentiary standards set by these cases."
        ),
        expected_output=(
            "A Legal Precedents Report in the following format:\n"
            "## Relevant Legal Precedents\n"
            "### Landmark Cases\n"
            "(For each: Case Name | Court & Year | Key Facts | Ratio Decidendi | "
            "Applicability to Current Case)\n"
            "### How These Precedents Help\n"
            "(For the complainant / For the accused)"
        ),
        agent=agent,
        context=context_tasks,
    )


def build_drafting_task(agent: Agent, context_tasks: list) -> Task:
    return Task(
        description=(
            "Using ALL the information gathered by the previous agents — the case intake "
            "report, the IPC sections analysis, and the legal precedents — produce a "
            "comprehensive, professionally formatted legal document.\n\n"
            "Your task is to produce ONE unified legal advisory document that contains:\n"
            "1. **Executive Summary**: Brief overview of the legal situation.\n"
            "2. **Case Facts**: Key facts as determined by intake.\n"
            "3. **Legal Analysis**: Applicable IPC sections with explanations.\n"
            "4. **Relevant Precedents**: Key judgments and their applicability.\n"
            "5. **Recommended Legal Remedies**: Step-by-step actions the complainant "
            "should take (file FIR, send legal notice, file petition, etc.).\n"
            "6. **Draft Legal Notice / FIR Draft** (whichever is most appropriate): "
            "A ready-to-use draft document.\n"
            "7. **Important Disclaimer**: This document is AI-generated for informational "
            "purposes only and must be reviewed by a qualified advocate before use.\n\n"
            "The document must be professional, clear, and understandable to a layperson."
        ),
        expected_output=(
            "A complete Legal Advisory Document formatted with clear sections and "
            "professional language. Must include:\n"
            "- Executive Summary\n"
            "- Case Facts\n"
            "- Legal Analysis (IPC Sections)\n"
            "- Relevant Precedents\n"
            "- Recommended Legal Remedies (numbered steps)\n"
            "- Draft Legal Notice OR Draft FIR\n"
            "- Legal Disclaimer\n"
            "Total length: 600-1200 words."
        ),
        agent=agent,
        context=context_tasks,
    )
