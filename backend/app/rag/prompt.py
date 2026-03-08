
SYSTEM_PROMPT = """
you are an AI assistant for IIIT Kottayam.
Answer only using the provided context.
If the answer is not persent, say: 
"I don`t have enough information to answer that, Excuse me, Thank You...."
"""


def build_prompt(context: str, question: str) -> str:
    return f"""
    {SYSTEM_PROMPT}
    Context: {context}
    Question: {question}
    Answer:
    """