from threading import Thread
from models import TelegramParserModel
from view import TelegramParserView

class TelegramParserController:
    def __init__(self, root):
        self.model = TelegramParserModel()
        self.view = TelegramParserView(root)

        self.view.browse_btn.config(command=self.view.browse_file)
        self.view.folder_browse_btn.config(command=self.view.browse_folder)
        self.view.start_btn.config(command=self.start_parsing)
        self.view.stop_btn.config(command=self.stop_parsing)

    def start_parsing(self):
        pass

    def stop_parsing(self):
        pass



