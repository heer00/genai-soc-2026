# 📄 DocBuddy Pro

DocBuddy Pro is a Retrieval-Augmented Generation (RAG) application that allows users to upload multiple PDF documents and ask questions across them. The application retrieves relevant document chunks using embeddings and ChromaDB, then uses Groq LLM to generate grounded answers with source citations.

---

# 🚀 Features

* Upload multiple PDF documents
* Automatic document chunking
* HuggingFace embeddings (`all-MiniLM-L6-v2`)
* ChromaDB vector storage
* Retrieval-Augmented Generation (RAG)
* Source citations with page numbers
* Retrieved Context viewer
* Anti-hallucination prompting
* Persistent vector database

---

# 🧠 What is RAG?

Retrieval-Augmented Generation (RAG) combines information retrieval with large language models.

Instead of relying only on the model's training data, relevant document chunks are retrieved from a vector database and supplied as context before generating an answer.

This helps produce more accurate, grounded, and explainable responses.

---

# 🛠️ Tech Stack

* Python
* Gradio
* LangChain
* HuggingFace Embeddings
* ChromaDB
* Groq API
* PyPDF
* python-dotenv

---

# 📂 Project Structure

```text
DocBuddy/
│
├── app.py
├── rag.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/heer00/genai-soc-2026.git
cd genai-soc-2026/week2/DocBuddy
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Run the application:

```bash
python app.py
```

---

# 🔄 How It Works

1. Upload PDF documents.
2. Load PDFs using `PyPDFLoader`.
3. Split documents into chunks using `RecursiveCharacterTextSplitter`.
4. Generate embeddings using `all-MiniLM-L6-v2`.
5. Store embeddings in ChromaDB.
6. Retrieve relevant chunks for a user query.
7. Send retrieved context to Groq LLM.
8. Generate a grounded answer with citations.

---

# 🧪 Testing

## Test 1 — Document Question

**Question**

```text
Summarize the story of Aron Ralston.
```

**Result**

The application successfully retrieved relevant chunks and generated a grounded summary with source citations.

📸 Add Screenshot Here

---

## Test 2 — Specific Question

**Question**

```text
How did Aron escape?
```

**Result**

The application retrieved the relevant context and answered correctly using document content.

📸 Add Screenshot Here

---

## Test 3 — Hallucination Prevention

**Question**

```text
What is the capital of France?
```

**Expected Result**

```text
I don't have that information in the uploaded documents.
```

**Result**

The application correctly refused to answer because the information was not present in the uploaded PDFs.

📸 Add Screenshot Here

---

## Test 4 — Retrieved Context Panel

The retrieved chunks were displayed inside the context panel, showing exactly what information was used to answer the query.

📸 Add Screenshot Here

---

# ✅ What Worked Well

* Multi-document indexing
* ChromaDB integration
* Source citations
* Grounded prompting
* Retrieved context transparency

---

# 🔧 Challenges Faced

* Gradio compatibility issues
* ChromaDB persistence handling
* Retrieval quality when PDFs contained both story content and worksheet questions
* Prompt grounding and hallucination prevention

---

# 🚀 Future Improvements

* Streaming responses
* Conversation memory
* Per-document filtering
* Hybrid search
* Chunk analytics dashboard
* Better retrieval ranking

---

# 📚 Learning Outcomes

Through this project, I learned:

* How embeddings represent text as vectors
* Why chunking is important in RAG systems
* How vector databases perform similarity search
* How retrieval quality affects answer quality
* How to build an end-to-end RAG pipeline using LangChain, ChromaDB, and Groq

---

Created as part of the **GenAI SOC Week 2 Project**.
