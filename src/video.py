from src.channel import Channel


class Video:
    """Класс для ютуб-видео"""

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""

        self.video_id = video_id
        video_response = (
            Channel.youtube.videos()
            .list(part="snippet,statistics,contentDetails,topicDetails", id=self.video_id)
            .execute()
        )
        self.video_title = video_response["items"][0]["snippet"]["title"]
        self.url = "https://youtu.be/" + self.video_id
        self.view_count = video_response["items"][0]["statistics"]["viewCount"]
        self.like_count = video_response["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    """Класс для ютуб-видео в плейлисте."""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
