import chromadb
import ollama


# Connect ChromaDB
client = chromadb.PersistentClient(
    path="../chroma_db"
)


collection = client.get_or_create_collection(
    name="fama"
)


print("Jumlah data dalam Chroma:", collection.count())


def ask_fama(question):

    # Buat embedding untuk soalan
    question_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=question
    )


    # Cari dokumen berkaitan
    result = collection.query(
        query_embeddings=[
            question_embedding["embedding"]
        ],
        n_results=2
    )


    documents = result["documents"][0]


    print("\n===== CONTEXT DITEMUI =====")
    print(documents)
    print("============================")


    # Gabungkan context
    context = "\n\n".join(documents)


    # Hantar kepada Phi3
    response = ollama.chat(
        model="phi3",

        options={
            "temperature": 0.2,
            "num_ctx": 2048
        },

        messages=[
            {
                "role": "system",
                "content": """
                Anda ialah FAMA AI Assistant untuk portal rasmi FAMA Malaysia.

                Peraturan wajib:
                1. Jawab sepenuhnya dalam Bahasa Melayu Malaysia.
                2. Jangan gunakan Bahasa Indonesia.
                3. Gunakan hanya maklumat daripada konteks yang diberikan.
                4. Jangan tambah maklumat yang tiada dalam konteks.
                5. Gunakan gaya jawapan mesra seperti chatbot kerajaan.
                6. Jika maklumat tidak ditemui, jawab:
                "Maaf, maklumat tersebut tidak terdapat dalam pangkalan data FAMA."
                """
            },

            {
                "role": "user",
                "content": f"""
Konteks FAMA:

{context}


Soalan pengguna:

{question}


Jawapan:
"""
            }
        ]
    )


    return response["message"]["content"]



if __name__ == "__main__":

    while True:

        question = input("\nSoalan FAMA: ")

        if question.lower() == "exit":
            break


        answer = ask_fama(question)


        print("\nJawapan:")
        print(answer)