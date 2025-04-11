from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.backend.chatbot import generate_response

app = FastAPI()


class UserInput(BaseModel):
    user_message: str  # Message from the user


@app.get("/")
def read_root():
    return {"message": "Welcome to the most advanced AI !"}


@app.post("/chat/")
def chat_with_bot(user_input: UserInput):
    try:
        # Generate response from chatbot
        response = generate_response(user_input.user_message)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
