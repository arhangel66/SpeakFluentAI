import io

from gtts import gTTS

from app.tts.base import TextToSpeachBase


class TextToSpeachLocal(TextToSpeachBase):
    def get_speach_data(self, text):
        tts = gTTS(text=text, lang="en")
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        return audio_data
