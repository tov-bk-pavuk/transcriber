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
    {"role": "system", "content": "Ви український лінгвіст перекладач"},
    {"role": "user", "content": "Перекладіть наступний текст українською мовою"},
    {"role": "user", "content": ""},
]

GPT_TRANSLATE_PROMPT_EN = [
    {"role": "system", "content": "You are a professional translator, English native speaker"},
    {"role": "user", "content": "Translate the text below into English"},
    {"role": "user", "content": ""},
]

SLEEP_SECS = 10
