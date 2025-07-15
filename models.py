import os.path
from tkinter.messagebox import showerror

import requests
from requests import get, RequestException
from settings import SUPPORTED_CONTENT_TYPES
import re
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
        #pattern = rf'https.*\.(?:{extensions})'
        pattern = rf'https[^\s\'">]+\.(?:{extensions})(?=[^\w\./]|$)'
        d = re.findall(pattern, content, re.IGNORECASE)

        links_image = []
        for i in d:
            if i not in links_image and ' ' not in i:

                links_image.append(i)


        count = 1
        k = 1
        for link in links_image:
            filename = f'{count}_image.{link.split('.')[-1]}'
            save_path = os.path.join(save_folder, filename)

            if os.path.exists(save_path):

                callback(f'Файл уже существует {filename}', 'yellow')
                count += 1
                continue
            response = get(link, stream=True, timeout=10)
            try:
                with open(save_path, 'wb') as f:
                    for c in response.iter_content(1024):
                        f.write(c)
                callback(f' Сохранено: {filename}')
                k += 1
            except Exception as e:
                callback(f'Ошибка загрузки: {e}', 'red')
            count += 1
        return k

    def save_text_content(self,content,channel_folder, callback=None):
        pattern = r'<div class="tgme_widget_message_text.*?" dir="auto">(.*?)<\/div>'
        data = re.findall(pattern, content)

        text_folder = os.path.join(channel_folder, 'text')
        os.makedirs(text_folder, exist_ok=True)

        k = 1
        for i in data:
            filename = f'{k}_text.txt'
            save_path = os.path.join(text_folder, filename)
            if os.path.exists(save_path):
                k += 1
                callback(f'Файл уже существует {filename}')
                continue
            clear_text = re.sub(r'<[^>]+>', '', i)

            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(clear_text)
            callback(f'Текст сохранен в {filename}')
            k+=1




    def save_video_content(self,content, content_type, channel_folder, callback=None):
        pattern = r'https?://[^\s\'"]+\.mp4[^\s\'"]*'
        data = re.findall(pattern, content)
        data = list(set(data))
        if data:
            video_folder = os.path.join(channel_folder, 'video')
            os.makedirs(video_folder, exist_ok=True)
            k = 1
            for i in data:
                save_path = os.path.join(video_folder, f'{k}_video.mp4')
                if os.path.exists(save_path):
                    k += 1
                    callback(f'Видео уже существует {k}_video.mp4')
                    continue
                with requests.get(i, stream=True) as r:
                    r.raise_for_status()
                    with open(save_path, 'wb') as f:
                        for c in r.iter_content(chunk_size=8192):
                            f.write(c)
                callback(f'Видео успешно скачано: {save_path}')

                k += 1

