import typing
import openai

import config
from third_patry_libs.code_tools import call_counter

openai.api_key = config.API_KEY


@call_counter
def audio_transcribe(file: typing.BinaryIO, language: typing.Union["ru", "uk", "en"] = None):
    return openai.Audio.transcribe(
        model="whisper-1",
        file=file,
        language=language,
    )


@call_counter
def get_chat_gpt_completion(text: str, prompt: dict, lang_prompt: str = "English"):
    system_prompt = f"You are a professional translator. {lang_prompt} native speaker."
    user_prompt = f"Translate the text below into {lang_prompt}."
    prompt[0].update({"content": system_prompt})
    prompt[1].update({"content": user_prompt})
    prompt[2].update({"content": text})
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
    )["choices"][0]["message"]["content"]


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
