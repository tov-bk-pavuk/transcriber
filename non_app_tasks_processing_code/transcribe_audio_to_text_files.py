from datetime import datetime
import openai
import tempfile
from time import sleep

import config
from integrations.open_ai import (
    audio_transcribe,
    get_chat_gpt_completion,
)

from third_patry_libs.custom_functions import (
    calculate_segment_duration,
    get_file_lists,
    gpt_slice_text_into_pieces,
    split_audio_into_segments,
)

openai.api_key = config.API_KEY
mp3_file_name_list, txt_files_file_name_list = get_file_lists()
print(f"{mp3_file_name_list=},{txt_files_file_name_list=}")


def divide_and_transcribe(mp3_filepath: str, result_filename: str, segment_size_mb=10):
    date_stamp = datetime.now().strftime("%d.%m.%y-%H:%M:%S")
    audio, segment_duration_ms = calculate_segment_duration(mp3_filepath, segment_size_mb)
    segments = split_audio_into_segments(audio, segment_duration_ms)

    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp_file_container:
        for number, segment in enumerate(segments):
            segment.export(temp_file_container.name, format="mp3")
            print(f"segment_{number} exported to temporary file")
            with open(temp_file_container.name, "rb") as temp_file_obj:
                temp_file_obj.seek(0)
                transcript = audio_transcribe(temp_file_obj, "ru")
                print(f"{audio_transcribe.count=}")
                sleep(config.SLEEP_SECS)
                print(f"segment_{number} transcribed ")
                with open(f"{config.FILE_FOLDER}/transcribed_{result_filename}_ru{date_stamp}.txt", "a") as fil_obj:
                    print(f"{transcript['text']=}")
                    fil_obj.write(transcript["text"] + "\n\n")

                    # CODE TO TRANSLATE TEXT FROM AUDIO ON THE FLY
                    # with open(f"/home/master/Загрузки/transcribed_text_ua{date_stamp}.txt", "a") as fil_obj_:
                    #     translated_text_ua = get_chat_gpt_completion(transcript['text'],
                    #                                                  config.GPT_TRANSLATE_PROMPT_UA, "Ukrainian")
                    #     sleep(config.SLEEP_SECS)
                    #     print(f"{translated_text_ua=}")
                    #     fil_obj_.write(translated_text_ua + "\n\n")
                    # with open(f"/home/master/Загрузки/transcribed_text_en{date_stamp}.txt", "a") as fil_obj_:
                    #     translated_text_en = get_chat_gpt_completion(transcript['text'], config.GPT_TRANSLATE_PROMPT_EN)
                    #     sleep(config.SLEEP_SECS)
                    #     print(f"{translated_text_en=}")
                    #     fil_obj_.write(translated_text_en + "\n\n")
                    # with open(f"/home/master/Загрузки/summarized_text_ru{date_stamp}.txt", "a") as fil_obj_:
                    #     summarized_text = get_chat_gpt_completion(transcript['text'], config.GPT_SUMMARY_PROMPT_RU, "Russian")
                    #     print(f"{get_chat_gpt_completion.count=}")
                    #     sleep(config.SLEEP_SECS)
                    #     print(f"{summarized_text=}")
                    #     fil_obj_.write(summarized_text + "\n\n")
        print("Success!")


def translate_txt_to_ua_en(txt_filenames_list: list):
    for text_file_name in txt_filenames_list:
        try:
            with open(f"{config.FILE_FOLDER}/{text_file_name}", "r") as file_obj:
                source_text = file_obj.read()
        except UnicodeDecodeError as ex:  # if text not in UTF-8
            print(f"{ex=}")
            with open(f"{config.FILE_FOLDER}/{text_file_name}", "rb") as file_obj:
                source_text = file_obj.read().decode('Windows-1251')
        text_pieces: list = gpt_slice_text_into_pieces(source_text, config.CHARACTERS_AMOUNT)
        with open(f"{config.FILE_FOLDER}/ua_{text_file_name}", "a") as file_obj_:
            for text in text_pieces:
                res = get_chat_gpt_completion(text, config.GPT_TRANSLATE_PROMPT_UA, "Ukrainian")
                print(f"{get_chat_gpt_completion.count=}")
                print(f"{res=}")
                file_obj_.write(res)
        with open(f"{config.FILE_FOLDER}/en_{text_file_name}", "a") as file_obj_:
            for text in text_pieces:
                res = get_chat_gpt_completion(text, config.GPT_TRANSLATE_PROMPT_EN)
                print(f"{get_chat_gpt_completion.count=}")
                print(f"{res=}")
                file_obj_.write(res)


if __name__ == "__main__":
    # TRANSCRIBE LIST OF AUDIO FILES INTO TEXT.TXT FILE IN RUSSIAN
    # for audio_file_filename in mp3_file_name_list:
    #     divide_and_transcribe(f"{config.FILE_FOLDER}/{audio_file_filename}", audio_file_filename, 15)

    # TRANSLATE LIST OF TEXT FILES INTO UKRAINIAN AND ENGLISH
    translate_txt_to_ua_en(txt_files_file_name_list)
