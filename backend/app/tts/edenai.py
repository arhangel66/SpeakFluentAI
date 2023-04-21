import base64
import io

from app.tts.base import TextToSpeachBase

key = "eyJhbGciOiJIUzI1NiIscookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql"


class EdentaiTTS(TextToSpeachBase):
    def get_speach_data(self, text):
        import json
        import requests

        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiN2NjNTVkNzUtYmQyZS00NTM3LTk0OWMtZDNiMGE3MmY2ZTM1IiwidHlwZSI6ImFwaV90b2tlbiJ9.qiagMO0DEuF8RNgxIBM8cQTiQIhK_Tnhs3zHZ2rb9fk"}

        url = "https://api.edenai.run/v2/audio/text_to_speech"
        payload = {
            "providers": "ibm",
            "settings": {"ibm": "en-US_LisaV3Voice"},
            "language": "en-US",
            "audio_format": "mp3",
            "option": "FEMALE",
            "text": text,
        }

        response = requests.post(url, json=payload, headers=headers)

        result = json.loads(response.text)

        audio_data = io.BytesIO()
        audio_str = result["ibm"]["audio"]
        audio_bytes = base64.b64decode(audio_str)

        # save to audio_data
        audio_data.write(audio_bytes)
        audio_data.seek(0)

        return audio_data
