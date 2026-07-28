import ollama


def generate_answer(question):

    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "system",
                "content": """
                Anda ialah FAMA AI Assistant.

                Tugas anda adalah menjawab soalan berkaitan FAMA.

                Arahan:
                - Gunakan HANYA maklumat daripada konteks yang diberikan.
                - Jangan mereka-reka fakta.
                - Jangan tambah maklumat luar.
                - Jawab dalam Bahasa Melayu yang mudah difahami.
                - Jika konteks tidak mempunyai jawapan, jawab:
                "Maaf, maklumat tersebut tidak ditemui dalam pangkalan data FAMA."
                - Gunakan format point jika sesuai.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]