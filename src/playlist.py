import datetime

import isodate

from src.channel import Channel


class PlayList:
    """
    Класс для ютуб-плейлиста
    """

    def __init__(self, playlist_id: str) -> None:
        """
        Экземпляр инициализируется ID плейлиста. Дальше все данные будут подтягиваться по API.
        """
        self.__id = playlist_id
        playlist_info = Channel.youtube.playlists().list(id=self.__id, part="snippet").execute()
        self.title = playlist_info["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/playlist?list=" + self.__id

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста.
        """

        playlist_videos = (
            Channel.youtube.playlistItems().list(playlistId=self.__id, part="contentDetails", maxResults=50).execute()
        )

        # получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video["contentDetails"]["videoId"] for video in playlist_videos["items"]]

        # Получаем длительность всех видеороликов из плейлиста и возвращаем суммарную длительность роликов
        video_response = (
            Channel.youtube.videos().list(part="contentDetails,statistics", id=",".join(video_ids)).execute()
        )

        total_duration = datetime.timedelta(0)
        for video in video_response["items"]:
            iso_8601_duration = video["contentDetails"]["duration"]
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self) -> str:
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        """

        playlist_videos = (
            Channel.youtube.playlistItems().list(playlistId=self.__id, part="contentDetails", maxResults=50).execute()
        )

        # получаем все id видеороликов из плейлиста
        video_ids: list[str] = [video["contentDetails"]["videoId"] for video in playlist_videos["items"]]

        # Получаем количество лайков всех видеороликов из плейлиста и возвращаем url ролика с максимальным количеством
        video_response = Channel.youtube.videos().list(part="statistics", id=",".join(video_ids)).execute()

        like_count: list[int] = [int(video["statistics"]["likeCount"]) for video in video_response["items"]]

        url_best_video = "https://youtu.be/" + video_response["items"][like_count.index(max(like_count))]["id"]

        return url_best_video
