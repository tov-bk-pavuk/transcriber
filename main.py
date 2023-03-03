import gradio as gr
import openai

import config
from custom_functions import transcribe, api_transcribe

openai.api_key = config.API_KEY


def main_processing_func(audio, file):
    return transcribe(audio), api_transcribe(file)


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
                file_input = gr.File(label="Download file")
                btn_submit = gr.Button(value="Transcribe")
            with gr.Column():
                text_output_record = gr.Textbox(label="Transcribed record")
                text_output_audio_file = gr.Textbox(label="Transcribed audio_file")
        btn_submit.click(
                fn=main_processing_func,
                inputs=[audio_input, file_input],
                outputs=[text_output_record, text_output_audio_file],
        )

    transcribe_interface.launch()
