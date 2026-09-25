import ollama

MODEL = "llama3.1:8b"


def chat(
    question: str,
    context: str,
    history: list
):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Answer the user's question using the provided "
                "document context and conversation history. "
                "If the answer is not present in the context, "
                "say that you could not find it in the documents."
            )
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": f"""
Context from documents:

{context}

Current question:

{question}
"""
        }
    )

    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    return response["message"]["content"]