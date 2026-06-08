from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("127-hours-992519.pdf")

pages = loader.load()

print("Total pages:", len(pages))

print("\nFirst page text:")
print(pages[0].page_content[:500])

print("\nMetadata:")
print(pages[0].metadata)
for i in range(3):
    print(f"\n--- PAGE {i+1} ---")
    print(pages[i].page_content[:200])