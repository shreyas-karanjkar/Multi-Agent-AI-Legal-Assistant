"""
ipc_search_tool.py
-------------------
ChromaDB-backed RAG tool for retrieving relevant IPC sections
given a natural language description of a legal case.
"""

import os
from typing import Type, Optional

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

import chromadb
from chromadb.utils import embedding_functions

# We import our IPC dataset
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.ipc_sections import IPC_SECTIONS


# ── ChromaDB Initialisation (done once, module-level) ────────────────────────

_CHROMA_COLLECTION_NAME = "ipc_sections"
_chroma_client = None
_ipc_collection = None


def _get_or_create_ipc_collection():
    """
    Uses the default sentence-transformer embedding function.
    """
    global _chroma_client, _ipc_collection

    if _ipc_collection is not None:
        return _ipc_collection

    # In-memory ChromaDB (ephemeral).  Swap to:
    #   chromadb.PersistentClient(path="./chroma_db")
    # if you want persistence across restarts.
    _chroma_client = chromadb.Client()

    # Use the default all-MiniLM-L6-v2 sentence-transformer embeddings
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Delete if already exists (fresh start on each app launch)
    try:
        _chroma_client.delete_collection(_CHROMA_COLLECTION_NAME)
    except Exception:
        pass

    _ipc_collection = _chroma_client.create_collection(
        name=_CHROMA_COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )

    # Ingest all IPC sections
    documents = []
    metadatas = []
    ids = []

    for idx, section in enumerate(IPC_SECTIONS):
        # Concatenate all fields to build a rich searchable document
        doc_text = (
            f"{section['section']}: {section['title']}. "
            f"{section['description']} "
            f"Keywords: {section['keywords']}. "
            f"Punishment: {section['punishment']}. "
            f"Category: {section['category']}."
        )
        documents.append(doc_text)
        metadatas.append(
            {
                "section": section["section"],
                "title": section["title"],
                "punishment": section["punishment"],
                "category": section["category"],
            }
        )
        ids.append(f"ipc_{idx}")

    _ipc_collection.add(documents=documents, metadatas=metadatas, ids=ids)
    return _ipc_collection


# ── Pydantic Input Schema ─────────────────────────────────────────────────────


class IPCSearchInput(BaseModel):
    query: str = Field(
        ...,
        description=(
            "A natural language description of the legal case or incident "
            "for which relevant IPC sections need to be retrieved."
        ),
    )
    top_k: Optional[int] = Field(
        default=2,
        description="Number of top IPC sections to retrieve (default 2).",
    )


# ── CrewAI Tool ───────────────────────────────────────────────────────────────


class IPCSectionSearchTool(BaseTool):
    """
    RAG-based IPC section retrieval tool backed by ChromaDB.
    Given a case description, it returns the most relevant IPC sections
    with their titles, descriptions, and applicable punishments.
    """

    name: str = "IPC Section Search Tool"
    description: str = (
        "Use this tool to search for relevant IPC (Indian Penal Code) sections "
        "based on a description of a legal case or incident. "
        "Provide a natural language description and the tool will return the "
        "top matching IPC sections with their details and applicable punishments."
    )
    args_schema: Type[BaseModel] = IPCSearchInput

    def _run(self, query: str, top_k: int = 5) -> str:
        """Retrieve the top-k most relevant IPC sections for the given query."""
        try:
            collection = _get_or_create_ipc_collection()

            results = collection.query(
                query_texts=[query],
                n_results=min(top_k, len(IPC_SECTIONS)),
            )

            if not results or not results["documents"] or not results["documents"][0]:
                return "No relevant IPC sections found for the given query."

            output_lines = [
                f"=== TOP {top_k} RELEVANT IPC SECTIONS ===\n"
            ]

            for i, (doc, meta, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                ),
                start=1,
            ):
                relevance_pct = round((1 - distance) * 100, 1)
                output_lines.append(
                    f"[{i}] {meta['section']} — {meta['title']}\n"
                    f"    Category  : {meta['category']}\n"
                    f"    Punishment: {meta['punishment']}\n"
                    f"    Relevance : {relevance_pct}%\n"
                    f"    Details   : {doc[:400]}...\n"
                )

            return "\n".join(output_lines)

        except Exception as exc:
            return f"Error while searching IPC sections: {exc}"
