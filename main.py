import mimetypes

import gradio as gr
import openai

from third_patry_libs.custom_functions import (
    audio_transcribe_to_text,
    translated_file_output,
    translated_temp_file_output,
    record_transcribe_to_text,
)
import config

openai.api_key = config.API_KEY


def translate_text(text):
    return translated_file_output(text)  # todo add second func with UA_PROMPT


def translate_text_file(txt_file):
    return translated_temp_file_output(txt_file)  # todo add second func with UA_PROMPT


def main_processing_func(record, audio_file):
    return record_transcribe_to_text(record), audio_transcribe_to_text(audio_file)


if __name__ == "__main__":
    # with gr.Blocks(css=".gradio-container {background-color: red}}") as transcribe_interface:
    with gr.Blocks(css="style.css") as transcribe_interface:
        with gr.Row():
            # with gr.Column():
            #     gr.Image("/home/master/Загрузки/63cc28a3459f07267c940575_map_6_elevation (2).jpg")
            # with gr.Accordion("See Details"):
            #     gr.Markdown("In the example above, the file argument is a Gradio gr.File() object passed to the process_file() function. Inside the function, we access the temporary filepath of the uploaded file by calling file.file.name. This returns a string containing the path to the temporary file, which can then be used for further processing.")
            with gr.Column():
                audio_input = gr.Audio(label="push to record here", source="microphone", type="filepath")
                audio_file_input = gr.File(label="Download audio_file")
                txt_file_input = gr.File(label="Download text_file")
                btn_submit = gr.Button(value="Transcribe")
                btn_translate = gr.Button(value="Translate")
                btn_translate_text_file = gr.Button(value="TransLATE txt file")
            with gr.Column():
                text_output_record = gr.Textbox(label="Transcribed record")
                text_output_audio_file = gr.Textbox(label="Transcribed audio_file")
                output_txt_file = gr.components.File(label="Загрузить файл")  # todo add ukrainian file
                # todo try to refactor with MIME type object
                output_translated_txt_file = gr.components.File(
                    label="Загрузить переведённый тхт файл",
                    # type="binary",
                    # file_types=["application/octet-stream"],
                )
        btn_submit.click(
            fn=main_processing_func,
            inputs=[audio_input, audio_file_input],
            outputs=[text_output_record, text_output_audio_file],
        )
        btn_translate.click(
            fn=translate_text,
            inputs=[text_output_audio_file],
            outputs=[output_txt_file],
        )
        btn_translate_text_file.click(
            fn=translate_text_file,
            inputs=[txt_file_input],
            outputs=[output_translated_txt_file],
        )

    transcribe_interface.launch()
