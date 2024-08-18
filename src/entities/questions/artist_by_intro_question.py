from typing import Dict, Optional

from src.entities.artist import Artist
from src.entities.question import Question
from src.entities.settings import Settings
from src.entities.track import Track


class ArtistByIntroQuestion(Question):
    def __init__(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings, group_id: Optional[int] = None) -> None:
        self.init_base(settings=settings, track_id=track.track_id, group_id=group_id)

        self.title = self.__get_title(track, artist_id2artist)
        self.answer = ", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists)

        self.question_timecode = f"0,{round(track.lyrics.lines[0].time - 1, 2)}"
        self.question_seek = 0
        self.answer_seek = None

    def __get_title(self, track: Track, artist_id2artist: Dict[int, Artist]) -> str:
        artist_types = [artist_id2artist[artist_id].artist_type.to_title() for artist_id in track.artists]

        if len(artist_types) == 1:
            return f"Назовите {artist_types[0]} по вступлению"

        return f'Назовите {", ".join(artist_types[:-1])} и {artist_types[-1]} по вступлению'
