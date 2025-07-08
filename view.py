import os.path
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import json


class TelegramParserView:

    def __init__(self, root):
        self.root = root
        self.root.title('Telegram Parser')
        self.root.geometry('700x500')

        self.root.iconbitmap('icon.ico')

        self.file_path_var = tk.StringVar()
        self.folder_path_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()

        self.contents_vars = {}

        self.create_widgets()
        self.setup_layout()

        if os.path.exists('file_browse.json'):
            with open('file_browse.json', 'r', encoding='utf-8') as f:
                file = json.load(f)
            file = file['file']
            self.file_path_var.set(file)
            self.file_entry.insert(0, self.file_path_var.get())

        if os.path.exists('folder_browse.json'):
            with open('folder_browse.json', 'r', encoding='utf-8') as f:
                file = json.load(f)
            file = file['file']
            self.folder_path_var.set(file)
            self.folder_entry.insert(0, self.folder_path_var.get())

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])

        if file_path:
            if os.path.exists('file_browse.json'):
                with open('file_browse.json', 'r', encoding='utf-8') as f:
                    file = json.load(f)
                file = file['file']
            else:
                d = {'file': file_path}

                with open('file_browse.json', 'w', encoding='utf-8') as f:
                    json.dump(d, f, indent=4)
                file = file_path

            self.file_path_var.set(file)
            self.file_entry.insert(0, self.file_path_var.get())
        return file_path

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            if os.path.exists('folder_browse.json'):
                with open('folder_browse.json', 'r', encoding='utf-8') as f:
                    file = json.load(f)
                file = file['file']
            else:
                d = {'file': folder_path}

                with open('folder_browse.json', 'w', encoding='utf-8') as f:
                    json.dump(d, f, indent=4)
                file = folder_path
            self.folder_path_var.set(file)
            self.folder_entry.insert(0, self.folder_path_var.get())
        return folder_path

    def create_widgets(self):
        self.file_frame = tk.LabelFrame(self.root, text='Файл с каналами telegram')
        self.file_entry = tk.Entry(self.file_frame, width=50)
        self.browse_btn = tk.Button(self.file_frame, text='Обзор...')

        self.folder_frame = tk.LabelFrame(self.root, text='Папка сохранения')
        self.folder_entry = tk.Entry(self.folder_frame, width=50)
        self.folder_browse_btn = tk.Button(self.folder_frame, text='Обзор...')

        self.content_frame = tk.LabelFrame(self.root, text='Tип контента для парсинга')
        content_types = ['images', 'videos', 'documents', 'audio', 'text']
        self.contents_vars = {ctype: tk.BooleanVar(value=True) for ctype in content_types}

        for c in content_types:
            # var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.content_frame, text=c, variable=self.contents_vars[c])
            cb.pack(side=tk.LEFT, padx=5)

        self.controll_frame = tk.Frame(self.root)
        self.start_btn = tk.Button(self.controll_frame, text='Начать парсинг')
        self.stop_btn = tk.Button(self.controll_frame, text='Остановить', state=tk.DISABLED)

        self.log_frame = tk.LabelFrame(self.root, text='Лог')
        self.log_text = tk.Text(self.log_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.log_scroll = tk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scroll.set)

        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100, mode='determinate')

    def setup_layout(self):
        self.file_frame.pack(pady=10, padx=10, fill=tk.X)
        self.file_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.browse_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.folder_frame.pack(pady=10, padx=10, fill=tk.X)
        self.folder_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.folder_browse_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.content_frame.pack(fill=tk.X, padx=5, pady=5)

        self.controll_frame.pack(pady=5, padx=5, fill=tk.X)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.log_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.progress_bar.pack(padx=5, pady=5, fill=tk.X)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def log_message(self, message, color='black'):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert('end', message + '\n', color)
        self.log_text.tag_config(color, foreground=color)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def get_selected_content_type(self):
        s = []
        for key, value in self.contents_vars.items():
            if value.get():
                s.append(key)

        return s

    def set_parsing_state(self, parsing):
        if parsing:
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
        else:
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update()
