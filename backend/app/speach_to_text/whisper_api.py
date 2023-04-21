import io
import tempfile

import openai

from common.config import API_KEY


def transcript_from_bytes(audio_bytes):
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3', delete=False) as temp_audio_file:
        openai.api_key = API_KEY
        temp_audio_file.write(audio_bytes)
        temp_audio_file.flush()

        with open(temp_audio_file.name, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, language='en')
            return transcript["text"]
