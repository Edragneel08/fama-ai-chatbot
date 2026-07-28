import chromadb
import ollama
from pypdf import PdfReader


# Lokasi PDF
pdf_path = "../data/FAMA_Profile.pdf"


# Baca PDF
reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    text += page.extract_text()


# =========================
# Text Chunking
# =========================

chunk_size = 500
overlap = 100

chunks = []

start = 0

while start < len(text):

    end = start + chunk_size

    chunk = text[start:end]

    chunks.append(chunk)

    start += chunk_size - overlap


print("Jumlah chunk:", len(chunks))


# =========================
# ChromaDB
# =========================

client = chromadb.PersistentClient(
    path="../chroma_db"
)


# delete collection lama
try:
    client.delete_collection("fama")
except:
    pass


collection = client.get_or_create_collection(
    name="fama"
)


# =========================
# Masukkan data
# =========================

for i, chunk in enumerate(chunks):

    embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )


    collection.add(
        ids=[
            f"fama_{i}"
        ],

        embeddings=[
            embedding["embedding"]
        ],

        documents=[
            chunk
        ]
    )


print("✅ Data FAMA berjaya masuk ChromaDB")
print("Jumlah dalam Chroma:", collection.count())