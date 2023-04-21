import time

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.gpt_conversation import Conversation
from app.schemas import Question
from app.common.logger import log, get_diff_time
from app.speach_to_text.whisper_api import transcript_from_bytes
from app.tts.edenai import EdentaiTTS
from app.tts.gtts import TextToSpeachLocal
from common import config

# from whisp import transcript_from_bytes

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
dicts = {"conversation": Conversation()}

tts_local_class = TextToSpeachLocal
tts_class = EdentaiTTS


@app.get("/start")
async def start() -> dict:
    t1 = time.time()
    dicts["conversation"] = Conversation()
    gpt_answer = dicts["conversation"].get_gpt_answer()
    log(f"/start, {get_diff_time(t1)},  {gpt_answer}")
    return {"text": gpt_answer}


@app.post("/speach-to-text")
async def speach_to_text(audio: UploadFile = File(...)):
    t1 = time.time()
    audio_content = await audio.read()
    transcript = transcript_from_bytes(audio_content)
    log(f"/speach-to-text, {get_diff_time(t1)},  {transcript}")
    return {"text": transcript}


@app.post("/ask")
async def ask(question: Question):
    t1 = time.time()
    answer = dicts["conversation"].process_user_message(question.text)
    log(f"/ask, {get_diff_time(t1)},  {answer}")
    return {"answer": answer}


@app.get("/text-to-speech")
async def text_to_speech(text: str):
    t1 = time.time()
    audio_data = tts_class().get_speach_data(text)

    log(f"/text- {get_diff_time(t1)}, to-speech, {text}")
    return StreamingResponse(audio_data, media_type="audio/mp3")


@app.get("/ping")
async def ping():
    return {"ping": config.API_KEY[:10]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
