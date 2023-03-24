from collections import namedtuple
from datetime import datetime
import math
from os import listdir, fstat
from tempfile import NamedTemporaryFile

import numpy as np
import openai
from pydub import AudioSegment

import config
from integrations.open_ai import (
    audio_transcribe,
    get_chat_gpt_completion,
)
from third_patry_libs.custom_exceptions import SizeException
from third_patry_libs.debug_tools import measure_time

openai.api_key = config.API_KEY


def record_transcribe_to_text(audio):
    if audio:
        with open(audio, "rb") as audio_file:
            file_size = fstat(audio_file.fileno()).st_size
            if file_size > config.BYTES_25:
                raise SizeException(f"Record size is {file_size / config.FILE_DIVIDER} Mb."
                                        f"Allowed record size is {config.BYTES_25 / config.FILE_DIVIDER} Mb!")
            transcript = audio_transcribe(audio_file)
            return transcript["text"]
    return "No audio"


def audio_transcribe_to_text(temp_file_obj):
    if temp_file_obj:
        file_path = temp_file_obj.name
        with open(file_path, "rb") as audio_file:
            file_size = fstat(audio_file.fileno()).st_size
            if file_size > config.FILE_SIZE_RESTRICTION_BYTES:
                raise SizeException(f"Reduce audio file size to"
                                        f" {config.FILE_SIZE_RESTRICTION_BYTES / config.FILE_DIVIDER} Mb!")
            elif file_size > config.BYTES_25:
                audio, segment_duration = calculate_segment_duration(
                    file_path, config.API_AUDIOFILE_SIZE_RESTRICTION_MB)
                segments = split_audio_into_segments(audio, segment_duration)
                transcribed_text = ""
                for segment in segments:
                    with NamedTemporaryFile(suffix=".mp3", mode="wb") as temp_file_container:
                        file_name = temp_file_container.name
                        segment.export(file_name, format="mp3")
                        with open(file_name, "rb") as fil_obj:
                            transcript = audio_transcribe(fil_obj)
                            transcribed_text += transcript["text"]
                transcribed_text_file_name = make_txt_transcribed_file(transcribed_text)
                return transcribed_text, transcribed_text_file_name
            else:
                transcript = audio_transcribe(audio_file)
                transcribed_text_file_name = make_txt_transcribed_file(transcript["text"])
                return transcript["text"], transcribed_text_file_name
    return "No file", None


def calculate_segment_duration(mp3_filepath: str, segment_size_mb: int):
    #  -> tuple[AudioSegment, int] Huggingface has Python 3.8
    # read MP3 file
    audio = AudioSegment.from_file(mp3_filepath, format="mp3")
    # calculate segment duration in milliseconds to achieve desired file size
    segment_duration_ms = math.ceil(
        (segment_size_mb * 1024 * 1024 * 8) / audio.frame_rate / audio.sample_width / audio.channels) * 1000
    return audio, segment_duration_ms


def split_audio_into_segments(audio: AudioSegment, segment_duration_ms: int) -> list:
    segments = []
    for i in range(0, len(audio), segment_duration_ms):
        segment = audio[i: i + segment_duration_ms]
        segments.append(segment)
    print("split_audio_into_segments is done")
    return segments


def divide_mp3_into_segments(mp3_filepath: str, segment_size_mb: int):
    audio, segment_duration_ms = calculate_segment_duration(mp3_filepath, segment_size_mb)
    segments = split_audio_into_segments(audio, segment_duration_ms)
    # export each segment to a new file
    for segment in segments:
        date_stamp = datetime.now().strftime("%d.%m.%y-%H:%M:%S.%f")
        segment.export(f"{config.FILE_FOLDER}/segment_{date_stamp}.mp3", format="mp3")


# for reducing file size
def convert_mp3_file_to_int_16(input_filepath: str, output_filepath: str, file_format: str = "mp3"):
    # read MP3 file
    audio_data = AudioSegment.from_file(input_filepath, format=file_format)
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
    processed_audio_data.export(output_filepath, format=file_format)


def make_txt_translated_file_from_pieces(text_pieces: list, lang: str = "English") -> str:
    if text_pieces:
        with NamedTemporaryFile(
                suffix=".txt", mode="a", delete=False, dir="flagged/file") as temp_file_container:
            for text_piece in text_pieces:
                print(text_piece)
                translated_text = get_chat_gpt_completion(text_piece, config.GPT_TRANSLATE_PROMPT_EN, lang)
                temp_file_container.write(translated_text)
        return temp_file_container.name  # todo investigate mime types to return


def make_txt_transcribed_file(text: str) -> str:
    with NamedTemporaryFile(
            suffix=".txt", mode="a", delete=False, dir="flagged/file") as temp_file_container:
        temp_file_container.write(text)
    return temp_file_container.name


def translated_temp_file_output(temp_file_obj, lang: str = "English"):
    if temp_file_obj:
        try:
            with open(temp_file_obj.name, "r") as file_obj:
                text = file_obj.read()
                check_text_restriction(text)
        except UnicodeDecodeError as ex:  # if text not in UTF-8
            print(f"{ex=}")
            with open(temp_file_obj.name, "rb") as file_obj:
                text = file_obj.read().decode('Windows-1251')
                check_text_restriction(text)
        text_pieces = gpt_slice_text_into_pieces(text, config.CHARACTERS_AMOUNT)
        return make_txt_translated_file_from_pieces(text_pieces, lang)


def make_txt_translated_file(text, lang: str = "English"):
    if text:
        check_text_restriction(text)
        text_pieces = gpt_slice_text_into_pieces(text, config.CHARACTERS_AMOUNT)
        return make_txt_translated_file_from_pieces(text_pieces, lang)


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


def check_text_restriction(text):
    text_length = len(text)
    if text_length > config.MAX_CHARACTERS:
        raise SizeException(f"Text has {text_length} characters when max {config.MAX_CHARACTERS} is allowed!")


def get_file_lists(folder_path: str = config.FILE_FOLDER):
    file_list = listdir(folder_path)
    FileList = namedtuple("FileList", "txt_file_names, mp3_file_names")
    return FileList([file_name for file_name in file_list if file_name.endswith(".mp3")],
                    [file_name for file_name in file_list if file_name.endswith(".txt")])
