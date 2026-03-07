# =========================================================================
# RAG PIPELINE ORCHESTRATOR(This file controls the flow of the rag system)
# =========================================================================
from .retriever import retrieve_context 
#Defining a function that accepts the query that was in string datatype and gives the output in formatted data as a dictionary
def run_rag_pipeline(query: str) -> dict:
    """
    Controls high-level RAG flow
    """
    # Step 1 — Retrieve relevant context
    context_chunks = retrieve_context(query)

    """(Generation step added in later weeks)
    (we will add LLM answer in generation later right now we only retrieve context and return it)
    """
    return{
        "query" : query,
        "context" : context_chunks,
        "answer" : "Generation step not implemented yet."
    }