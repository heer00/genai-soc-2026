import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# =========================
# GROQ
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# CHROMA + EMBEDDINGS
# =========================

CHROMA_DIR = "./chroma_store"

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = None


# =========================
# LOAD EXISTING DB
# =========================

def load_existing_store():
    global vectorstore

    if os.path.exists(CHROMA_DIR):
        try:
            vectorstore = Chroma(
                persist_directory=CHROMA_DIR,
                embedding_function=embedding_model
            )
            return True

        except Exception as e:
            print(f"Error loading ChromaDB: {e}")

    return False


# =========================
# INDEX DOCUMENTS
# =========================

def index_docments(pdf_files):
    global vectorstore

    all_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    for pdf in pdf_files:

        pdf_path = pdf.name
        filename = Path(pdf_path).name

        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        chunks = splitter.split_documents(pages)

        for chunk in chunks:

            chunk.metadata["source"] = filename

            chunk.metadata["page"] = (
                chunk.metadata.get("page", 0) + 1
            )

        all_chunks.extend(chunks)

    print(f"\nIndexed {len(all_chunks)} chunks")

    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR
    )

    return len(all_chunks)


# =========================
# ASK QUESTION
# =========================

def ask(question):
    global vectorstore

    if vectorstore is None:
        return (
            "No documents indexed yet.",
            "Please upload and index PDFs first."
        )

    docs = vectorstore.similarity_search(
        query=question,
        k=15
    )

    context = ""
    context_display = ""
    sources_used = []

    print("\n" + "=" * 80)
    print("RETRIEVED DOCUMENTS")
    print("=" * 80)

    for i, doc in enumerate(docs, start=1):

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "?"
        )

        print(f"\nChunk {i}")
        print(doc.page_content[:300])

        sources_used.append(
            f"{source} (Page {page})"
        )

        context += (
            f"\n\n[{source} - Page {page}]\n"
            f"{doc.page_content}"
        )

        preview = doc.page_content[:300]

        context_display += (
            f"### {source} (Page {page})\n\n"
            f"{preview}\n\n"
            f"---\n\n"
        )

    prompt = f"""
You are a document assistant.

Rules:
1. Answer ONLY using the provided context.
2. If the answer is not present in the context, say:
   "I don't have that information in the uploaded documents."
3. Do not use outside knowledge.
4. Cite relevant information from the context.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    unique_sources = sorted(
        set(sources_used)
    )

    answer += "\n\n### Sources\n"

    for src in unique_sources:
        answer += f"- {src}\n"

    return answer, context_display

