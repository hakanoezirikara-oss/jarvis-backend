import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# .env Datei laden
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("WARNUNG: Kein OPENAI_API_KEY in der .env gefunden!")

client = OpenAI(api_key=api_key)

app = FastAPI(title="Aureus Media - Jarvis Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryModel(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "Jarvis Core is online", "brand": "Aureus Media"}

@app.post("/jarvis")
def ask_jarvis(query: QueryModel):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist Jarvis, die universelle, hochpräzise KI-Schnittstelle von Aureus Media."},
                {"role": "user", "content": query.prompt}
            ]
        )
        answer = response.choices[0].message.content
        return {"response": answer, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))