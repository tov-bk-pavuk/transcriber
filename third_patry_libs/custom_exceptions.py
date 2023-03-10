from gradio import exceptions as gr_ex


class FileSizeException(gr_ex.Error):
    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)
