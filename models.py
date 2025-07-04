from tkinter.messagebox import showerror
from requests import get, RequestException
import re
from settings import SUPPORTED_CONTENT_TYPES


class TelegramParserModel:
    def __init__(self):
        self.parsing = False
        self.stop_parsing = False

    def load_channels(self, file_path):
        channels = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i in f.readlines():
                    channels.append(i.strip())
                return channels
        except Exception as e:
            showerror('Ошибка', f'Не удалось прочитать файл {e}')

    def get_channel_content(self, channel_url):
        try:
            response = get(channel_url)
            response.raise_for_status()

            return response.text
        except RequestException as e:
            showerror('Ошибка', f'Ошибка при загрузке контента канала {channel_url}: {e}')

    def save_media_content(self, content, content_type, save_folder, callback=None):
        if content_type not in SUPPORTED_CONTENT_TYPES:
            showerror('Ошибка', f'Не поддерживается тип контента для парсинга')
            return
        extensions = '|'.join(SUPPORTED_CONTENT_TYPES[content_type])
        pattern = rf'https?://[^\s]+?\.(?:{extensions})(?:\?[^\s]*)?'
        d = re.findall(pattern, content, re.IGNORECASE)
        print(d)
