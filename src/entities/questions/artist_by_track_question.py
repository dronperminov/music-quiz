import random
from typing import Dict, Optional

from src.entities.artist import Artist
from src.entities.question import Question
from src.entities.settings import Settings
from src.entities.track import Track


class ArtistByTrackQuestion(Question):
    def __init__(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings, group_id: Optional[int] = None) -> None:
        self.init_base(settings=settings, track_id=track.track_id, group_id=group_id)

        self.title = self.__get_title(track, artist_id2artist)
        self.answer = ", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists)

        self.question_timecode = ""
        self.question_seek = self.__get_question_seek(track)
        self.answer_seek = None

    def __get_title(self, track: Track, artist_id2artist: Dict[int, Artist]) -> str:
        artist_types = [artist_id2artist[artist_id].artist_type.to_title() for artist_id in track.artists]

        if len(artist_types) == 1:
            return f"Назовите {artist_types[0]}"

        return f'Назовите {", ".join(artist_types[:-1])} и {artist_types[-1]}'

    def __get_question_seek(self, track: Track) -> float:
        if track.lyrics is None or not track.lyrics.lrc:
            return 0

        line = random.choice(track.lyrics.lines[:len(track.lyrics) * 3 // 4])
        return line.time