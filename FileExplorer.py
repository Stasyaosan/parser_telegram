import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json


class File_Explorer:
    def __init__(self, root):
        self.root = root
        self.root.title('Проводник файлов')
        self.root.geometry('500x500')
        self.create_widgets()
        if os.path.exists('folder_browse.json'):
            with open('folder_browse.json', 'r', encoding='utf-8') as f:
                file = json.load(f)
            self.dir = file['file']
        self.update_file_list()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=('Size', 'Type'), selectmode='browse')
        self.tree.heading('#0', text='Имя')
        self.tree.heading('Size', text='Размер')
        self.tree.heading('Type', text='Тип')

        self.tree.column('#0', width=300)
        self.tree.column('Size', width=100)
        self.tree.column('Type', width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind('<Double-1>', self.on_double_click)

    def on_double_click(self):
        pass

    def update_file_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if self.dir == None:
            return
        try:
            # parent_dir = os.path.dirname(self.dir)
            items = os.listdir(self.dir)
            dirs = []
            files = []
            for d in items:
                if os.path.isdir(os.path.join(self.dir, d)):
                    dirs.append(d)

            for f in items:
                if not os.path.isdir(os.path.join(self.dir, f)):
                    files.append(f)

            for d in sorted(dirs):
                self.tree.insert('', 'end', text=d, values=('', 'Папка'), tags=('dir',))

            for f in sorted(files):
                pass

        except:
            return


root = tk.Tk()
app = File_Explorer(root)
root.mainloop()
