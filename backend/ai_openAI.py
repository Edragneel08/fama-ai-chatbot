from openai import OpenAI
from backend.config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def generate_answer(question):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
                Anda ialah FAMA AI Assistant.
                Jawab soalan berkaitan FAMA,
                pertanian dan agro makanan dalam Bahasa Melayu.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )


    return response.choices[0].message.content