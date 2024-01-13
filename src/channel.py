import json
import os

import googleapiclient.discovery
from dotenv import load_dotenv
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    load_dotenv()
    api_key: str | None = os.getenv("YT_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        channel = Channel.youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + channel["items"][0]["id"]
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls) -> googleapiclient.discovery.Resource:
        """
        Возвращает объект для работы с YouTube API.
        """
        return Channel.youtube

    def to_json(self, filepath: str) -> json:
        """
        Сохраняет в ".json" файл значения атрибутов экземпляра `Channel`
        """
        with open(filepath, "w", encoding="UTF-8") as f:
            json.dump(self.__dict__, f)
