from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
loader = PyPDFLoader("127-hours-992519.pdf")
pages = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(pages)

print("Pages:", len(pages))
print("Chunks:", len(chunks))

print("\nMetadata:")
print(chunks[0].metadata)

print("\nChunk Preview:")
print(chunks[0].page_content[:300])