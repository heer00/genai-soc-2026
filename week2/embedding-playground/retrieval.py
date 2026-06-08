from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
question = "How was Aron trapped?"

vectorstore = Chroma(
    persist_directory="./chroma_store",
    embedding_function=embedding_model
)
results = vectorstore.similarity_search_with_score(
    question,
    k=3
)

for i, (doc, score) in enumerate(results, start=1):
    print("=" * 80)
    print(f"Result {i}")
    print("Score:", score)
    print("Metadata:", doc.metadata)
    print()
    print(doc.page_content[:500])