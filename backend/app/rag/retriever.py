# =================#
# RETRIEVAL MODULE #
# =================#
# This imports List from Python's typing system
from typing import List


def retrieve_context(query: str) -> List[str]:
    """
    Retrieves relevant context chunks for a given user query.
    """
    results = []

    context_chunks = [doc["content"] for doc in results]

    return context_chunks