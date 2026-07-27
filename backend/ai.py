import ollama


def generate_answer(question):

    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "system",
                "content": """
                Anda ialah FAMA AI Assistant.

                FAMA ialah Lembaga Pemasaran Pertanian Persekutuan
                di Malaysia.

                Fungsi FAMA:
                - membantu pemasaran produk pertanian
                - membantu petani dan usahawan agro makanan
                - mengurus pembangunan pasaran agro makanan
                - memperkenalkan produk tempatan ke pasaran

                Jawab dalam Bahasa Melayu.
                Jika tidak tahu, nyatakan tidak mempunyai maklumat.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]