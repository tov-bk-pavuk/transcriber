from datetime import datetime
import openai
import tempfile

import config
from custom_functions import (
    calculate_segment_duration,
    split_audio_into_segments

)

openai.api_key = config.API_KEY


def divide_and_transcribe(mp3_filepath: str, segment_size_mb=10):
    date_stamp = datetime.now().strftime("%d.%m.%y-%H:%M:%S")
    audio, segment_duration_ms = calculate_segment_duration(mp3_filepath, segment_size_mb)
    segments = split_audio_into_segments(audio, segment_duration_ms)

    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file_container:
        for segment in segments:
            segment.export(temp_file_container.name, format="mp3")
            with open(temp_file_container.name, "rb") as temp_file_obj:
                temp_file_obj.seek(0)
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=temp_file_obj,
                    language="ru",
                )
                with open(f"/home/master/Загрузки/transcribed_text_seg_{date_stamp}.txt", "a") as fil_obj:
                    print(f"{transcript['text']=}")
                    fil_obj.write(transcript["text"] + "\n\n")
        print("Success!")


if __name__ == "__main__":
    file_name = "segment_2.mp3"
    file_path = f"/home/master/Загрузки/{file_name}"
    divide_and_transcribe(file_path, 4)
