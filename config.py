import os
from dotenv import load_dotenv

load_dotenv()

MODE = ""  # "prod" is you need authorization turn on

API_KEY = os.getenv("OPENAI_API_KEY", "")
USERS = [
    (os.getenv("pm_username", ""), os.getenv("pm_password", "")),
    (os.getenv("guest_username", ""), os.getenv("guest_password", "")),
]

GPT_SUMMARY_PROMPT_EN = [
    {"role": "system", "content": "You are a summarization expert who makes takeaways from daily meetings."},
    {"role": "user", "content": "Write a summary of the text below, and use numbered points to outline the "
                                "most important information"},
    {"role": "user", "content": ""},
]

GPT_TRANSLATE_PROMPT = [
    {"role": "system", "content": "You are a professional translator. English native speaker."},
    {"role": "user", "content": "Translate the text below into English."},
    {"role": "user", "content": ""},
]

GPT_SUMMARY_PROMPT_RU = [
    {"role": "system", "content": "Ты умеешь структурировать тексты"},
    {"role": "user", "content": "Подели текст на абзацы по смыслу. Озаглавь каждый абзац и оформи его в виде "
                                "маркированного списка утверждений."},
    {"role": "user", "content": ""},
]

GPT_TRANSLATE_PROMPT_UA = [
    {"role": "system", "content": f"You are a professional translator. Ukrainian native speaker."},
    {"role": "user", "content": "Translate the text below into Ukrainian."},
    {"role": "user", "content": ""},
]

GPT_TRANSLATE_PROMPT_EN = [
    {"role": "system", "content": "You are a professional translator. English native speaker."},
    {"role": "user", "content": "Translate the text below into English."},
    {"role": "user", "content": ""},
]

SLEEP_SECS = 3

FILE_FOLDER = "/home/master/Загрузки/transcribe_and_translate"

LANGUAGES = ["English", "Ukrainian", "Russian"]

# need to divide text into parts because of 4096 tokens restriction
CHARACTERS_AMOUNT = 4000
API_AUDIOFILE_SIZE_RESTRICTION_MB = 25
BYTES_25: int = 25000000
FILE_SIZE_RESTRICTION_BYTES = 50000000
FILE_DIVIDER = 1000000  # to get Mb
MAX_CHARACTERS = 25000  # text size restriction

SOME_TEXT = "In the example above, the file argument is a Gradio gr.File()"
" object passed to the process_file() function. Inside the function,"
" we access the temporary filepath of the uploaded file by calling file.file.name."
" This returns a string containing the path to the temporary file,"
" which can then be used for further processing."
