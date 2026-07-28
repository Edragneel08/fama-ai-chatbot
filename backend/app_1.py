from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
chat_history = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "FAMA AI Chatbot API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    question = request.question.lower()

    if any(word in question for word in [
        "apa itu fama",
        "siapa fama",
        "mengenai fama",
        "tentang fama"
    ]):
        answer = """
        FAMA ialah Lembaga Pemasaran Pertanian Persekutuan. FAMA merupakan agensi yang membantu pembangunan pemasaran produk pertanian dan industri agro makanan.
        """

    elif any(word in question for word in [
        "fungsi",
        "peranan",
        "tugas"
    ]):
        answer = """
        Fungsi utama FAMA adalah membantu pemasaran,
        pengedaran dan pembangunan produk agro makanan.
        FAMA juga membantu pengeluar pertanian memasarkan
        produk mereka kepada pengguna.
        """

    elif any(word in question for word in [
        "produk",
        "jualan",
        "agro"
    ]):
        answer = """
        FAMA membantu pemasaran pelbagai produk pertanian
        termasuk hasil tanaman, makanan agro dan produk
        usahawan pertanian.
        """

    elif "lokasi" in question or "alamat" in question:
        answer = """
        Maklumat lokasi dan alamat pejabat FAMA boleh
        dirujuk melalui portal rasmi FAMA.
        """

    else:
        answer = """
        Maaf, saya masih belum mempunyai maklumat berkaitan
        soalan tersebut. Cuba tanya berkaitan FAMA,
        fungsi, peranan atau produk pertanian.
        """

    chat_history.append({
        "question": request.question,
        "answer": answer.strip()
    })

    return {
        "question": request.question,
        "answer": answer.strip(),
        "history": chat_history
    }


@app.get("/history")
def history():
    return {
        "conversation": chat_history
    }