import io

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from gpt_conversation import Conversation
from whisp import transcript_from_bytes

# from whisper import asr

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key
dicts = {"conversation": None}


@app.get("/start")
async def start() -> dict:
    dicts["conversation"] = Conversation()
    gpt_answer = dicts["conversation"].get_gpt_answer()
    return {"text": gpt_answer}


@app.post("/speach-to-text")
async def speach_to_text(audio: UploadFile = File(...)):
    audio_content = await audio.read()
    transcript = transcript_from_bytes(audio_content)
    return {"text": transcript}


class Question(BaseModel):
    text: str


@app.post("/ask")
async def ask(question: Question):
    answer = dicts["conversation"].process_user_message(question.text)
    return {"answer": answer}


@app.get("/text-to-speech")
async def text_to_speech(text: str):
    tts = gTTS(text=text, lang="en")
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return StreamingResponse(audio_data, media_type="audio/mp3")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
