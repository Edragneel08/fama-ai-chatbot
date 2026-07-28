import chromadb
import ollama


# ==========================
# CONNECT CHROMADB
# ==========================

client = chromadb.PersistentClient(
    path="../chroma_db"
)


collection = client.get_collection(
    name="fama"
)


print(
    f"Jumlah data dalam ChromaDB: {collection.count()}"
)



# ==========================
# SYSTEM PROMPT
# ==========================

SYSTEM_PROMPT = """

Anda ialah FAMA AI Assistant untuk portal rasmi FAMA Malaysia.

Tugas anda ialah menjawab soalan pengguna berdasarkan konteks rasmi FAMA yang diberikan sahaja.

PERATURAN WAJIB:

1. Jawab dalam Bahasa Melayu Malaysia.
2. Jangan gunakan Bahasa Indonesia.
3. Jangan gunakan pengetahuan luar daripada konteks.
4. Jangan mereka-reka fakta atau membuat andaian.
5. Gunakan hanya maklumat yang berkaitan dengan soalan pengguna.
6. Abaikan maklumat dalam konteks yang tidak berkaitan dengan soalan.
7. Baca keseluruhan konteks sebelum menjawab, jangan hanya mengambil ayat pertama.
8. Kekalkan nama program, istilah rasmi dan senarai penting FAMA.
9. Jangan menambah penerangan yang tiada dalam konteks.
10. Jika pengguna meminta penjelasan lanjut, gunakan maklumat tambahan yang terdapat dalam konteks sahaja.
11. Jangan gunakan bullet point jika soalan pengguna tidak meminta senarai.
12. Bila respon ke soalan pengguna, gunakan format point jika sesuai dan saiz font yang sesuai.


FORMAT JAWAPAN:

Gunakan Markdown.

Untuk soalan "Apa itu / Apakah":

- Berikan definisi utama dahulu.
- Sertakan maklumat tambahan yang berkaitan jika ada dalam konteks.
- Jangan masukkan tujuan, objektif atau fungsi kecuali terdapat dalam soalan pengguna.

Untuk soalan fungsi / tujuan / objektif:

- Gunakan bullet point.
- Setiap isi mesti berada pada baris berasingan.
- Jangan gabungkan beberapa isi dalam satu ayat.

Untuk program atau inisiatif FAMA:

- Terangkan maksud program.
- Terangkan tujuan.
- Senaraikan komponen atau aktiviti yang terdapat dalam konteks.

Jika maklumat tidak terdapat dalam konteks:

"Maaf, maklumat tersebut tidak terdapat dalam pangkalan data FAMA."

"""


# ==========================
# CLEAN OUTPUT
# ==========================

def clean_answer(answer):


    answer = answer.replace(
        "•",
        "-"
    )


    answer = answer.replace(
        ". -",
        ".\n-"
    )


    # Betulkan bullet bercantum

    answer = answer.replace(
        "- ",
        "\n- "
    )


    return answer.strip()



# ==========================
# ASK FAMA
# ==========================

def ask_fama(question):


    # ----------------------
    # EMBEDDING QUESTION
    # ----------------------

    question_embedding = ollama.embeddings(

        model="nomic-embed-text",

        prompt=question

    )



    # ----------------------
    # SEARCH CHROMA
    # ----------------------

    result = collection.query(

        query_embeddings=[
            question_embedding["embedding"]
        ],


        n_results=3,


        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )



    documents = []


    print("\n==============================")
    print("CONTEXT DITEMUI")
    print("==============================")



    for doc, meta, distance in zip(

        result["documents"][0],

        result["metadatas"][0],

        result["distances"][0]

    ):


        print(
            "\nDistance:",
            round(distance,3)
        )


        print(
            doc[:200]
        )



        # FILTER
        # ambil yang relevan sahaja

        if distance < 0.75:

            documents.append(doc)



    print("==============================")



    if len(documents) == 0:


        return (
            "Maaf, maklumat tersebut tidak terdapat "
            "dalam pangkalan data FAMA."
        )




    # ----------------------
    # BUILD CONTEXT
    # ----------------------


    context = ""


    for i,doc in enumerate(documents):

        context += f"""

--- Maklumat {i+1} ---

{doc}

"""




    # ----------------------
    # SEND TO LLAMA
    # ----------------------


    response = ollama.chat(


        model="llama3.2",


        options={

            "temperature":0.2,

            "num_ctx":4096

        },


        messages=[


            {
                "role":"system",

                "content":SYSTEM_PROMPT

            },


            {

                "role":"user",

                "content":f"""

Konteks rasmi FAMA:


{context}


Soalan pengguna:

{question}


Sila jawab berdasarkan konteks sahaja.

"""

            }


        ]

    )



    answer = response["message"]["content"]



    answer = clean_answer(
        answer
    )



    return answer





# ==========================
# API FUNCTION
# ==========================

def chat_fama(question):

    return ask_fama(question)




# ==========================
# TEST TERMINAL
# ==========================

if __name__ == "__main__":


    print(
        "\n========== FAMA AI =========="
    )


    while True:


        question = input(
            "\nSoalan FAMA: "
        )


        if question.lower()=="exit":

            break



        answer = ask_fama(
            question
        )


        print(
            "\nJawapan:\n"
        )


        print(answer)