from datetime import datetime
import numpy as np
import math
from pydub import AudioSegment
import openai
from time import sleep
import pprint as p

import config

openai.api_key = config.API_KEY


def chat_gpt_create_answer():
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )


def transcribe(audio):
    if audio:
        with open(audio, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript["text"]
    return "No audio"


def api_transcribe(temp_file_obj):
    if temp_file_obj:
        file_path = temp_file_obj.name
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript["text"]
    return "No file"


def api_transcribe_to_txt_file(file_path):
    date_stamp = datetime.now().strftime("%d.%m.%y-%H:%M:%S")
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        with open(f"/home/master/Загрузки/transcribed_text_seg_{date_stamp}.txt", "w") as fil_obj:
            fil_obj.write(transcript["text"])
        print("Success!")


def convert_mp3_file():
    # read MP3 file
    audio_data = AudioSegment.from_file("input_audio.mp3", format="mp3")

    # get sample rate and channels
    sample_rate = audio_data.frame_rate
    channels = audio_data.channels

    # get raw audio data in bytes format
    raw_audio_data = audio_data.raw_data

    # convert raw audio data to numpy array
    numpy_array = np.frombuffer(raw_audio_data, dtype=np.int16)

    # do some processing with the audio data...

    # convert numpy array back to raw bytes
    processed_raw_data = numpy_array.tobytes()

    # create a new AudioSegment object from the processed raw data
    processed_audio_data = AudioSegment(
        data=processed_raw_data,
        sample_width=2,  # 16-bit audio
        frame_rate=sample_rate,
        channels=channels
    )

    # write the processed audio data to an MP3 file
    processed_audio_data.export("output_audio.mp3", format="mp3")


def divide_mp3_into_segments(mp3_filepath: str, segment_size_mb: int):
    audio, segment_duration_ms = calculate_segment_duration(mp3_filepath, segment_size_mb)

    segments = split_audio_into_segments(audio, segment_duration_ms)

    # export each segment to a new file
    for segment in segments:
        date_stamp = datetime.now().strftime("%d.%m.%y-%H:%M:%S.%f")
        segment.export(f"/home/master/Загрузки/segment_{date_stamp}.mp3", format="mp3")


def split_audio_into_segments(audio: AudioSegment, segment_duration_ms: int) -> list:
    segments = []
    for i in range(0, len(audio), segment_duration_ms):
        segment = audio[i: i + segment_duration_ms]
        segments.append(segment)
    return segments


def calculate_segment_duration(mp3_filepath: str, segment_size_mb: int) -> tuple[AudioSegment, int]:
    # read MP3 file
    audio = AudioSegment.from_file(mp3_filepath, format="mp3")
    # calculate segment duration in milliseconds to achieve desired file size
    segment_duration_ms = math.ceil(
        (segment_size_mb * 1024 * 1024 * 8) / audio.frame_rate / audio.sample_width / audio.channels) * 1000
    return audio, segment_duration_ms


if __name__ == "__main__":
    filepath = "/home/master/Загрузки/segment_03.03.23-19:27:32.136620.mp3"
    # filepath = "/home/master/Загрузки/segment_03.03.23-19:27:25.248100.mp3"
    # filepath = "/home/master/Загрузки/segment_03.03.23-19:27:19.229522.mp3"
    api_transcribe_to_txt_file(filepath)
