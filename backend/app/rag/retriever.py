# =================#
# RETRIEVAL MODULE #
# =================#
# This imports List from Python's typing system
from typing import List

# Defining a function that takes a query must be in string format and return list of decimal numbers as vector embeddings
def embed_query(query : str) -> List[float]:
    """
    Temporary code for embedding logic
    (Module 4 will provide real embeddings)
    """
    #Prints message to console to indicate that the query is being embedded
    print("Embedding query...")
    #Sends results back to the caller 
    return [0.1, 0.2, 0.3]  # mock vector(Fake embedding for testing)

# Defining a function that takes a list of decimal numbers as vector embeddings and returns matched documents in form of list of dictionaries 
def search_vector_db(query_vector: List[float]) -> List[dict]:
    """
    Placeholder for vector DB search
    (Module 4 will implement this)
    """
    #Prints message to console to indicate that the vector database is being searched
    print("Searching vector database...")

    # Mock search results(The following data is fake and is used for testing purposes)
    return [
        {"content": "RAG combines retrieval and generation."},
        {"content": "Vector databases store embeddings."},
        {"content": "LLMs generate answers using context."}
    ]

# Defining a function that takes a query in string format and returns a list of relevant context chunks in string format
def retrieve_context(query: str) -> List[str]:
    """
    Full retrieval flow:
    Query → Embedding → Vector Search → Context
    """

    # Step 1 — Convert query to embedding(Text to vector conversion)
    query_vector = embed_query(query)

    # Step 2 — Search vector database(Finding relevant documents based on the query vector)
    results = search_vector_db(query_vector)

    # Step 3 — Extract text content(Extracting the "content" field from each document in the search results)
    context_chunks = [doc["content"] for doc in results]
    #Returns the list of relevant context chunks back to the caller
    return context_chunks