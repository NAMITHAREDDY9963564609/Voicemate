from TTS.api import TTS
from pydub import AudioSegment

tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

def generate_reply(text, speaker_wav, output_path, language="en"):
    cleaned = speaker_wav.replace(".wav", "_cleaned.wav")
    audio = AudioSegment.from_file(speaker_wav)
    audio.set_channels(1).set_frame_rate(22050).export(cleaned, format="wav")

    tts.tts_to_file(
        text=text,
        speaker_wav=cleaned,
        language=language,
        file_path=output_path
    )
