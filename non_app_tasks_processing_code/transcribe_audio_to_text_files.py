from datetime import datetime
import openai
import tempfile
from time import sleep

import config
from third_patry_libs.custom_functions import (
    calculate_segment_duration,
    get_chat_gpt_completion,
    split_audio_into_segments

)

openai.api_key = config.API_KEY


def divide_and_transcribe(mp3_filepath: str, segment_size_mb=10):
    date_stamp = datetime.now().strftime("%d.%m.%y-%H:%M:%S")
    audio, segment_duration_ms = calculate_segment_duration(mp3_filepath, segment_size_mb)
    segments = split_audio_into_segments(audio, segment_duration_ms)

    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file_container:
        for number, segment in enumerate(segments):
            segment.export(temp_file_container.name, format="mp3")
            print(f"segment_{number} exported to temporary file")
            with open(temp_file_container.name, "rb") as temp_file_obj:
                temp_file_obj.seek(0)
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=temp_file_obj,
                    language="ru",
                )
                # sleep(config.SLEEP_SECS)
                print(f"segment_{number} transcribed ")
                # with open(f"/home/master/Загрузки/transcribed_text_ru{date_stamp}.txt", "a") as fil_obj:
                #     print(f"{transcript['text']=}")
                #     fil_obj.write(transcript["text"] + "\n\n")
                # with open(f"/home/master/Загрузки/transcribed_text_ua{date_stamp}.txt", "a") as fil_obj:
                #     translated_text_ua = get_chat_gpt_completion(transcript['text'], config.GPT_TRANSLATE_PROMPT_UA)
                #     sleep(config.SLEEP_SECS)
                #     print(f"{translated_text_ua=}")
                #     fil_obj.write(translated_text_ua + "\n\n")
                # with open(f"/home/master/Загрузки/transcribed_text_en{date_stamp}.txt", "a") as fil_obj:
                #     translated_text_en = get_chat_gpt_completion(transcript['text'], config.GPT_TRANSLATE_PROMPT_EN)
                #     sleep(config.SLEEP_SECS)
                #     print(f"{translated_text_en=}")
                #     fil_obj.write(translated_text_en + "\n\n")
                with open(f"/home/master/Загрузки/summarized_text_ru{date_stamp}.txt", "a") as fil_obj:
                    summarized_text = get_chat_gpt_completion(transcript['text'], config.GPT_SUMMARY_PROMPT_RU)
                    sleep(config.SLEEP_SECS)
                    print(f"{summarized_text=}")
                    fil_obj.write(summarized_text + "\n\n")
        print("Success!")


if __name__ == "__main__":
    file_name = "segment_2.mp3"
    file_path = f"/home/master/Загрузки/{file_name}"
    divide_and_transcribe(file_path, 4)
