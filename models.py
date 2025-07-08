import os.path
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
        pattern = rf'https[^\s\'">]+\.(?:{extensions})(?=[^\w\./]|$)'
        d = re.findall(pattern, content, re.IGNORECASE)
        links_image = []

        for i in d:
            if i not in links_image and ' ' not in i:
                links_image.append(i)

        count = 1
        for link in links_image:
            filename = f'{count}.{link.split('.')[-1]}'

            save_path = os.path.join(save_folder, filename)
            if os.path.exists(save_path):
                callback(f'Файл {filename} уже существует', '#ff801f')
                count += 1
                continue
            response = get(link, stream=True, timeout=10)
            try:
                with open(save_path, 'wb') as f:
                    for c in response.iter_content(1024):
                        f.write(c)
            except Exception as e:
                callback(f'Ошибка загрузки: {e}', '#ff381f')
            count += 1
        return count
