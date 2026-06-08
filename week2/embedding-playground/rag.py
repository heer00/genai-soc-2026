import os
from dotenv import load_dotenv
from groq import Groq

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="./chroma_store",
    embedding_function=embedding_model
)
def ask_document(question: str):
    print(f"\nQuestion: {question}")

    # Retrieve top chunks
    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    print("\nRetrieved Chunks:")
    print("=" * 80)

    context_parts = []

    for i, doc in enumerate(docs, start=1):
        page = doc.metadata.get("page", "?")
        source = doc.metadata.get("source", "Unknown")

        print(f"\n[Chunk {i}]")
        print(f"Source: {source} | Page: {page}")
        print(doc.page_content[:250])
        print("-" * 50)

        context_parts.append(
            f"[Source {i}: {source}, Page {page}]\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": """
You are a document assistant.

Rules:
1. Answer ONLY using the provided context.
2. If the answer is not present in the context, say exactly:
   "I don't have that information in the uploaded documents."
3. Do not use your general knowledge.
4. At the end, provide the sources used.
"""
        },
        {
            "role": "user",
            "content": f"""
Context:

{context}

Question:
{question}
"""
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )

    print("\nAnswer:")
    print("=" * 80)
    print(response.choices[0].message.content)

while True:
    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    ask_document(question)