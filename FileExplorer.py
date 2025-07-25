import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
from settings import SUPPORTED_CONTENT_TYPES
from tkinter import messagebox
import cv2


class File_Explorer:
    def __init__(self, root):
        self.root = root
        self.root.title('Проводник файлов')
        self.root.geometry('700x600')
        self.dir = None
        self.parent_dir = None
        self.create_widgets()
        if os.path.exists('folder_browse.json'):
            with open('folder_browse.json', 'r', encoding='utf-8') as f:
                file = json.load(f)
            self.dir = file['file']
            self.parent_dir = file['file']
        self.update_file_list()

    def create_widgets(self):
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(self.container, columns=('Image', 'Size', 'Type'), selectmode='browse')

        self.tree.heading('#0', text='Имя')
        self.tree.heading('Size', text='Размер')
        self.tree.heading('Type', text='Тип')

        self.tree.column('#0', width=300)
        self.tree.column('Size', width=100)
        self.tree.column('Type', width=100)

        vsb = ttk.Scrollbar(self.container, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label='Удалить', command=self.delete_item)
        self.context_menu.add_command(label='Открыть', command=self.open_item)

    def delete_item(self):
        pass

    def open_item(self):
        pass

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def on_double_click(self, event):
        try:
            item = self.tree.selection()[0]
            name = self.tree.item(item, 'text')
            if name == '..':
                self.go_up()
            else:
                full_path = os.path.join(self.dir, name).replace(' ', '')
                if os.path.isdir(full_path):
                    self.dir = full_path
                    self.update_file_list()
                else:
                    self.open_file(full_path)
        except:
            pass

    def open_file(self, full_path):
        type_ = self.get_file_type(full_path)
        try:
            if self.get_file_type(full_path) == 'Изображение':
                self.show_image(full_path)
            elif type_ == 'Текст':
                self.show_text(full_path)
            elif type_ == 'Видео':
                self.show_video(full_path)
            else:
                messagebox.showerror('Непонятен тип файла')
        except:
            pass

    def show_video(self, full_path):
        top = tk.Toplevel(self.root)
        top.title(os.path.basename(full_path))
        top.geometry(f'800x600')
        top.config(background='#fff')
        self.video_label = tk.Label(top)
        self.video_label.pack()

        self.play_video(full_path)

    def play_video(self, path):
        c = cv2.VideoCapture(path)

        def update_frame():
            ret, frame = c.read()
            if ret:
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                self.video_label.after(10, update_frame)
            else:
                c.release()

        update_frame()

    def show_text(self, path):
        top = tk.Toplevel(self.root)
        top.title(os.path.basename(path))
        top.geometry(f'800x600')
        top.config(background='#fff')
        with open(path, encoding='utf-8') as f:
            text_ = f.read()

        scrollbar = tk.Scrollbar(top)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(top, yscrollcommand=scrollbar.set, font=(None, 18), wrap=tk.WORD, highlightthickness=0,
                       relief='flat')
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar.config(command=text.yview)

        text.insert(tk.END, text_)
        text.config(state=tk.DISABLED)

    def show_image(self, path):
        top = tk.Toplevel(self.root)
        top.title(os.path.basename(path))
        width = top.winfo_screenwidth()
        height = top.winfo_screenheight()
        top.geometry(f'{width}x{height}')
        img = Image.open(path)
        img.thumbnail((800, 600))
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=photo)
        label.image = photo
        label.pack(expand=True)

    def go_up(self):
        d = '/'.join(self.dir.split('\\')[:-1])
        self.dir = d
        if d == '':
            self.dir = self.parent_dir
        else:
            self.dir = d
        self.update_file_list()

    def update_file_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if self.dir == None:
            return
        try:
            if self.parent_dir != self.dir:
                self.tree.insert('', 'end', text='..', values=('', 'Папка'), tags=('dir',))
            items = os.listdir(self.dir)
            dirs = []
            files = []
            for d in items:
                if os.path.isdir(os.path.join(self.dir, d)):
                    dirs.append(d)

            for f in items:
                if not os.path.isdir(os.path.join(self.dir, f)):
                    files.append(f)

            folder_img = Image.open('icons/folder.png')
            self.folder_icon = ImageTk.PhotoImage(folder_img.resize((16, 16)))

            for d in sorted(dirs):
                self.tree.insert('', 'end', text=f' {d}',
                                 values=('', 'Папка'),
                                 image=self.folder_icon, tags=('dir',))

            image_img = Image.open('icons/image.png')
            self.image_icon = ImageTk.PhotoImage(image_img.resize((16, 16)))

            for f in sorted(files):
                full_path = os.path.join(self.dir, f)
                size = self.get_size(os.path.getsize(full_path))
                file_type = self.get_file_type(f)
                if file_type == 'Изображение':
                    self.tree.insert('', 'end', text=f, image=self.image_icon, values=(size, file_type), tags=('img',))
                else:
                    self.tree.insert('', 'end', text=f, values=(size, file_type), tags=('file',))

        except:
            pass

    def get_size(self, size):
        for i in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{round(size, 2)} {i}'
            size = size / 1024
        return f'{size:1.f} TB'

    def get_file_type(self, filename):
        e = filename.split('.')[-1]
        if e in SUPPORTED_CONTENT_TYPES['text']:
            return 'Текст'
        elif e in SUPPORTED_CONTENT_TYPES['images']:
            return 'Изображение'
        elif e in SUPPORTED_CONTENT_TYPES['videos']:
            return 'Видео'
        else:
            return 'Файл'


root = tk.Tk()
app = File_Explorer(root)
root.mainloop()
