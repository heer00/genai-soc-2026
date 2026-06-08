from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer('all-MiniLM-L6-v2')

sentence1 = "I Love Programming"
sentence2 = "Programming is my passion"
sentence3 = "The sky is blue"

emb1 = model.encode(sentence1)
emb2 = model.encode(sentence2)
emb3 = model.encode(sentence3)

sim12 = util.cos_sim(emb1, emb2)
sim13 = util.cos_sim(emb1, emb3)

print(f"Similarity between sentence 1 and 2: {sim12.item():.4f}")
print(f"Similarity between sentence 1 and 3: {sim13.item():.4f}")   

print(len(emb1))