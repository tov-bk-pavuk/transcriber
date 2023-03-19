import os

from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
)
import config


class GetAudio:
    az_key = config.AZ_KEY_1
    az_region = config.AZ_REGION
    speech_config = SpeechConfig(subscription=az_key, region=az_region)

    def __init__(self, voice: str):  # voices are defined in config.py
        self.speech_config.speech_synthesis_voice_name = voice
        self.audio_config = None
        self.speech_synthesizer = None

    def set_filename(self, audio_folder_path, filename):
        self.audio_config = AudioOutputConfig(filename=f"{audio_folder_path}/{filename}")
        self.speech_synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

    def get_voices(self):
        result_future_obj = self.speech_synthesizer.get_voices_async().get()
        for voice in result_future_obj.voices:
            print(voice.short_name)


def get_text_from_file(filepath):
    with open(filepath, "r") as f_obj:
        return f_obj.read(), f_obj.name


def run():
    text, file_name = get_text_from_file(f"{config.FILE_FOLDER}/test_txt_to_voice_ru.txt")
    print(text)
    audio = GetAudio(config.VOICES.get("ru"))
    audio.set_filename(config.FILE_FOLDER_TTS, "test_02.wav")
    audio.speech_synthesizer.speak_text_async(text).get()
    # os.system(f'mpv --start=0  "{file_path}"')


if __name__ == "__main__":
    run()
