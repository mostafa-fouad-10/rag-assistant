def build_rag_prompt(context: str, query: str) -> str:


    return f"""


    You are a helpful assistant answering questions based on provided documents.

    Instructions:

    * Answer the user's question using only the provided context.
    * Do not use outside knowledge.
    * If the answer cannot be found in the context, say:
    "I couldn't find the answer in the provided documents."
    * Do not make up or assume information.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """.strip()
