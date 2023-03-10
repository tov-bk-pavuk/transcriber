import gradio as gr
import logging
import openai

from third_patry_libs.custom_functions import (
    audio_transcribe_to_text,
    make_txt_translated_file,
    translated_temp_file_output,
    record_transcribe_to_text,
)
import config

openai.api_key = config.API_KEY
logging.basicConfig(level=logging.CRITICAL)


def launch_mode(func, mode: str):
    return func(auth=config.USERS, auth_message="Enter login and password") if mode == "prod" else func()


def translate_text(text, lang):
    return make_txt_translated_file(text, lang)


def translate_text_file(txt_file, lang):
    return translated_temp_file_output(txt_file, lang)


def transcribe_record(record):
    return record_transcribe_to_text(record)


def transcribe_audiofile(audio_file):
    return audio_transcribe_to_text(audio_file)


if __name__ == "__main__":
    with gr.Blocks(css="style.css", analytics_enabled=True) as transcribe_interface:
        with gr.Tab("Record and transcribe"):
            with gr.Row():
                with gr.Column():
                    audio_input = gr.Audio(label="push to record here", source="microphone", type="filepath")
                    btn_transcribe_record = gr.Button(value="Transcribe record")
                with gr.Column():
                    text_output_record = gr.Textbox(label="Transcribed record", placeholder="Тут будет транскрибация")
        with gr.Tab("Audiofile transcribe"):
            with gr.Row():
                with gr.Column():
                    audio_file_input = gr.File(label="Upload audio_file")
                    btn_transcribe_audiofile = gr.Button(value="Transcribe audio_file")
                with gr.Column():
                    text_output_audio_file = gr.Textbox(
                        label="Transcribed audio_file",
                        placeholder="Тут будет транскрибация или введите текст",
                    )
                    lang_input_dropdown = gr.components.Dropdown(choices=config.LANGUAGES, label="Select language")
                    btn_translate = gr.Button(value="Translate text upper")
                    output_txt_file = gr.components.File(label="Download txt file")
        with gr.Tab("Text file translate"):
            with gr.Row():
                with gr.Column():
                    txt_file_input = gr.File(label="Upload text_file")
                    input_dropdown = gr.components.Dropdown(choices=config.LANGUAGES, label="Select language")
                    btn_translate_text_file = gr.Button(value="Translate txt file")
                    # todo try to refactor with MIME type object
                with gr.Column():
                    output_translated_txt_file = gr.components.File(
                        label="Download translated txt file",
                        # type="binary",
                        # file_types=["application/octet-stream"],
                    )
        btn_transcribe_record.click(
            fn=transcribe_record,
            inputs=[audio_input],
            outputs=[text_output_record],
        )
        btn_transcribe_audiofile.click(
            fn=transcribe_audiofile,
            inputs=[audio_file_input],
            outputs=[text_output_audio_file],
        )
        btn_translate.click(
            fn=translate_text,
            inputs=[text_output_audio_file, lang_input_dropdown],
            outputs=[output_txt_file],
        )
        btn_translate_text_file.click(
            fn=translate_text_file,
            inputs=[txt_file_input, input_dropdown],
            outputs=[output_translated_txt_file],
            api_name="translate_txt_file"
        )

    launch_mode(transcribe_interface.launch, config.MODE)
