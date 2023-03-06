import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY", "")

GPT_SUMMARY_PROMPT_EN = [
    {"role": "system", "content": "You are a summarization expert who makes takeaways from daily meetings."},
    {"role": "user", "content": "Write a summary of the text below, and use numbered points to outline the "
                                "most important information"},
    {"role": "user", "content": ""},
]

GPT_SUMMARY_PROMPT_RU = [
    {"role": "system", "content": "Ты мастер обобщения текстов. Умеешь отлично выделять"
                                  " главное из ежедневных звонков"},
    {"role": "user", "content": "Обобщи и создай структурированный текст, используя маркированный список"},
    {"role": "user", "content": ""},
]

GPT_TRANSLATE_PROMPT_UA = [
    {"role": "system", "content": "You are a professional multilanguage translator. Ukrainian native speaker."},
    {"role": "user", "content": "Please translate the text below into Ukrainian language."},
    {"role": "user", "content": ""},
]

GPT_TRANSLATE_PROMPT_EN = [
    {"role": "system", "content": "You are a professional translator, English native speaker."},
    {"role": "user", "content": "Please translate the text below into English language."},
    {"role": "user", "content": ""},
]

SLEEP_SECS = 3

FILE_FOLDER = "/home/master/Загрузки/transcribe_and_translate"
