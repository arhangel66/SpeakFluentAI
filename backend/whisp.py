import io
import tempfile

import whisper
import certifi
print(certifi.where())
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


# example:
import whisper

model = whisper.load_model("base")
# result = model.transcribe("response.mp3")
# print(result["text"])



def transcript_from_bytes(audio_bytes):
    model = whisper.load_model("base")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(audio_bytes)
        temp_file_path = temp_file.name
    options = {"language": 'en'}

    result = model.transcribe(temp_file_path, language='en')
    return result["text"]


