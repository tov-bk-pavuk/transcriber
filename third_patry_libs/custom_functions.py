from collections import namedtuple
from datetime import datetime
import math
import numpy as np
from os import listdir
from pydub import AudioSegment
import openai

import config
from integrations.open_ai import get_chat_gpt_completion

openai.api_key = config.API_KEY


def transcribe(audio):  # todo add audio slicing
    if audio:
        with open(audio, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript["text"]
    return "No audio"


def api_transcribe(temp_file_obj):  # todo add audio slicing
    if temp_file_obj:
        file_path = temp_file_obj.name
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript["text"]
    return "No file"


def translated_file_output(text):  # todo add text slicing
    if text:
        with open(f"{config.FILE_FOLDER}/1.txt", "w") as fil_obj:
            # todo make prompt as agr
            translated_text = get_chat_gpt_completion(text, config.GPT_TRANSLATE_PROMPT_EN)
            fil_obj.write(translated_text)
        return f"{config.FILE_FOLDER}/1.txt"


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
    print("split_audio_into_segments is done")
    return segments


def calculate_segment_duration(mp3_filepath: str, segment_size_mb: int) -> tuple[AudioSegment, int]:
    # read MP3 file
    audio = AudioSegment.from_file(mp3_filepath, format="mp3")
    # calculate segment duration in milliseconds to achieve desired file size
    segment_duration_ms = math.ceil(
        (segment_size_mb * 1024 * 1024 * 8) / audio.frame_rate / audio.sample_width / audio.channels) * 1000
    return audio, segment_duration_ms


def make_txt_file(path_to_new_file, txt_content):
    with open(path_to_new_file, "a") as file_obj:
        file_obj.write(txt_content)


def measure_time(func):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds to execute.")
        return result

    return wrapper


@measure_time
def slice_text_into_pieces(text: str, segment_size: int) -> list:
    start_index = 0
    stop_index = segment_size
    list_of_text_pieces = []
    for ind in range(0, len(text), segment_size):
        # measure text piece
        text_piece = text[start_index:stop_index]
        # search for the dot at the end of the piece and receive its index
        tail_index = text_piece[::-1].index(".")
        # cut the tail
        piece_cut_the_tail = text[start_index:stop_index - tail_index]
        # add piece to list
        list_of_text_pieces.append(piece_cut_the_tail)
        # get net start indexX
        start_index = stop_index - tail_index + 1
        # get new finish index
        stop_index += segment_size
    return list_of_text_pieces


@measure_time
def gpt_slice_text_into_pieces(text: str, segment_size: int) -> list:
    start_index = 0
    stop_index = segment_size
    list_of_text_pieces = []
    while start_index < len(text):
        if stop_index >= len(text):
            stop_index = len(text)
        else:
            # find last "." character before stop_index
            tail_index = text.rfind(".", start_index, stop_index)
            if tail_index != -1:
                stop_index = tail_index + 1
        # extract text piece
        text_piece = text[start_index:stop_index]
        list_of_text_pieces.append(text_piece)
        # update start_index and stop_index
        start_index = stop_index
        stop_index += segment_size
    return list_of_text_pieces


def get_file_lists(folder_path: str = config.FILE_FOLDER):
    file_list = listdir(folder_path)
    FileList = namedtuple("FileList", "txt_file_names, mp3_file_names")
    return FileList([file_name for file_name in file_list if file_name.endswith(".mp3")],
                    [file_name for file_name in file_list if file_name.endswith(".txt")])
