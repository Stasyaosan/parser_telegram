import os
from threading import Thread
from models import TelegramParserModel
from view import TelegramParserView
from tkinter import messagebox
from time import sleep


class TelegramParserController:
    def __init__(self, root):
        self.model = TelegramParserModel()
        self.view = TelegramParserView(root)

        self.view.browse_btn.config(command=self.view.browse_file)
        self.view.folder_browse_btn.config(command=self.view.browse_folder)
        self.view.start_btn.config(command=self.start_parsing)
        self.view.stop_btn.config(command=self.stop_parsing)

    def start_parsing(self):
        file_path = self.view.file_path_var.get()
        save_folder = self.view.folder_path_var.get()
        selected_types = self.view.get_selected_content_type()

        if not file_path:
            messagebox.showerror('Ошибка', 'Укажите файл с каналами Telegram')
            return
        if not selected_types:
            messagebox.showerror('Ошибка', 'Выберите хотя бы один тип контента')
            return

        try:
            channels = self.model.load_channels(file_path)
        except Exception as e:
            messagebox.showerror('Ошибка', 'Файл не содержит канадлов для парсинга')

        self.model.parsing = True
        self.model.stop_parsing = False
        self.view.set_parsing_state(True)
        self.view.clear_log()
        self.view.update_progress(0)

        Thread(target=self.parse_channels, args=(channels, save_folder, selected_types), daemon=True).start()

    def parse_channels(self, channels, save_folder, selected_types):
        total_channels = len(channels)
        for index, i in enumerate(channels):
            if self.model.stop_parsing:
                break
            self.view.log_message(f'\n Парсинг канала: {i}')
            self.view.update_progress(((index + 1) / total_channels) * 100)

            content = self.model.get_channel_content(i)

            channel_name = i.split('/')[-1]
            channel_folder = os.path.join(save_folder, channel_name)

            os.makedirs(channel_folder, exist_ok=True)

            for content_type in selected_types:
                if self.model.stop_parsing:
                    break

                if content_type == 'text':
                    self.model.save_text_content(
                        content,
                        channel_folder,
                        callback=self.view.log_message
                    )
                elif content_type == 'videos':
                    self.model.save_video_content(
                        content,
                        content_type,
                        channel_folder,
                        callback=self.view.log_message
                    )
                else:
                    count = self.model.save_media_content(
                        content,
                        content_type,
                        channel_folder,
                        callback=self.view.log_message
                    )
                    if count > 0:
                        self.view.log_message(f'Сохранено {count} файлов типа {content_type}')
        self.model.parsing = False
        self.view.update_progress(100)

        if not self.model.stop_parsing:
            self.view.log_message('\n Парсинг завершен!')
        else:
            self.view.log_message('\n Парсинг остановлен пользователем')

    def stop_parsing(self):
        self.model.stop_parsing = True
        self.view.log_message('Остановка парсинга...')
        self.view.set_parsing_state(False)
