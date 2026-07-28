from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from rag import chat_fama


app = FastAPI(
    title="FAMA AI Chatbot"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

    answer = chat_fama(
        request.question
    )

    return {
        "answer": answer
    }