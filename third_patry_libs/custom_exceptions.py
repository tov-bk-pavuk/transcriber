from gradio import exceptions as gr_ex


class SizeException(gr_ex.Error):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
