import chromadb
import ollama
from pypdf import PdfReader
import os
import re


# ==========================
# CONFIG
# ==========================

DATA_PATH = "../data"

CHROMA_PATH = "../chroma_db"

COLLECTION_NAME = "fama"


# ==========================
# TEXT CLEANING
# ==========================

def clean_text(text):

    if not text:
        return ""


    # Tukar bullet PDF kepada format baru
    text = text.replace("•", "\n-")

    text = text.replace("▪", "\n-")


    # Buang whitespace berlebihan
    text = re.sub(
        r'\s+',
        ' ',
        text
    )


    # Pastikan bullet turun line
    text = text.replace(
        "- ",
        "\n- "
    )


    return text.strip()



# ==========================
# READ ALL PDF
# ==========================

print("📄 Membaca semua PDF...")


pages = []


for pdf_file in os.listdir(DATA_PATH):

    if pdf_file.lower().endswith(".pdf"):


        pdf_path = os.path.join(
            DATA_PATH,
            pdf_file
        )


        print("➡️", pdf_file)


        reader = PdfReader(
            pdf_path
        )


        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):


            raw_text = page.extract_text()


            cleaned = clean_text(
                raw_text
            )


            if cleaned:


                pages.append(
                    {
                        "source": pdf_file,
                        "page": page_number,
                        "text": cleaned
                    }
                )



print(
    "Jumlah halaman:",
    len(pages)
)



# ==========================
# CHUNKING
# ==========================

chunk_size = 1000
overlap = 300


chunks = []


for page in pages:


    text = page["text"]

    source = page["source"]

    page_number = page["page"]


    start = 0


    while start < len(text):


        end = start + chunk_size


        chunk = text[start:end]


        chunks.append(
            {
                "text": chunk,
                "source": source,
                "page": page_number
            }
        )


        start += chunk_size - overlap



print(
    "Jumlah chunk:",
    len(chunks)
)



# ==========================
# CHROMADB SETUP
# ==========================

print(
    "🔄 Setup ChromaDB..."
)


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)



# Padam collection lama
try:

    client.delete_collection(
        COLLECTION_NAME
    )

    print(
        "Collection lama dipadam"
    )


except:

    pass



collection = client.create_collection(
    name=COLLECTION_NAME,

    metadata={
        "hnsw:space": "cosine"
    }
)



# ==========================
# INSERT DATA
# ==========================

print(
    "🚀 Masukkan data ke ChromaDB..."
)



for i, item in enumerate(chunks):


    text = item["text"]


    embedding = ollama.embeddings(

        model="nomic-embed-text",

        prompt=text

    )


    collection.add(

        ids=[
            f"fama_{i}"
        ],


        embeddings=[
            embedding["embedding"]
        ],


        documents=[
            text
        ],


        metadatas=[

            {
                "source": item["source"],

                "page": item["page"]

            }

        ]

    )


    print(
        f"Chunk {i+1}/{len(chunks)} selesai"
    )



# ==========================
# DONE
# ==========================

print("\n==========================")
print("✅ INGEST SELESAI")
print("==========================")


print(
    "Jumlah dalam ChromaDB:",
    collection.count()
)