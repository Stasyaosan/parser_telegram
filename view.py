import tkinter as tk
from tkinter import filedialog

class TelegramParserView:
    def __init__(self, root):
        self.root = root
        self.root.title('Telegram Parser')
        self.root.geometry('700x500')

        self.root.iconbitmap('icon.ico')

        self.create_widgets()
        self.setup_layout()

        self.file_path_var = tk.StringVar()
        self.folder_path_var = tk.StringVar()


    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
        if file_path:
            self.file_path_var.set(file_path)
            self.file_entry.insert(0, self.file_path_var.get())
        return file_path


    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_var.set(folder_path)
            self.folder_entry.insert(0, self.folder_path_var.get())
        return folder_path


    def create_widgets(self):
        self.file_frame = tk.LabelFrame(self.root, text='Файл с каналами telegram')
        self.file_entry = tk.Entry(self.file_frame, width=50)
        self.browse_btn = tk.Button(self.file_frame, text='Обзор...')

        self.folder_frame = tk.LabelFrame(self.root, text='Папка сохранения')
        self.folder_entry = tk.Entry(self.folder_frame, width=50)
        self.folder_browse_btn = tk.Button(self.folder_frame, text='Обзор...')

        self.content_frame = tk.LabelFrame(self.root, text='Тип контента для парсинга')
        content_types = ['images', 'videos', 'documents', 'audio', 'text']

        for c in content_types:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.content_frame, text=c, variable=var)
            cb.pack(side=tk.LEFT, padx=5)



    def setup_layout(self):
        self.file_frame.pack(pady=10, padx=10, fill=tk.X)
        self.file_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.browse_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.folder_frame.pack(pady=10, padx=10, fill=tk.X)
        self.folder_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.folder_browse_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.content_frame.pack(fill=tk.X, expand=True)