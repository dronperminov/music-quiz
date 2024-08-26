from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ArtistsAnalytics:
    correct: List[dict]
    incorrect: List[dict]
    correct_time: Dict[int, float]
    incorrect_time: Dict[int, float]

    @classmethod
    def create(cls: "ArtistsAnalytics", questions: List[dict], track_id2artist_ids: Dict[int, List[int]], top_count: int = 20, min_questions: int = 3) -> "ArtistsAnalytics":
        artists = {False: defaultdict(int), True: defaultdict(int)}
        time = {False: defaultdict(list), True: defaultdict(list)}

        for question in questions:
            if question["group_id"]:
                continue

            for artist_id in track_id2artist_ids[question["track_id"]]:
                artists[question["correct"]][artist_id] += 1

                if question["answer_time"]:
                    time[question["correct"]][artist_id].append(question["answer_time"])

        for key, key_artists in artists.items():
            sorted_artists = sorted([{"artist_id": artist_id, "count": count} for artist_id, count in key_artists.items()], key=lambda artist: -artist["count"])
            artists[key] = [artist for artist in sorted_artists if artist["count"] >= min_questions][:top_count]
            time[key] = {artist_data["artist_id"]: ArtistsAnalytics.mean(time[key][artist_data["artist_id"]]) for artist_data in artists[key]}

        return cls(
            correct=artists[True],
            incorrect=artists[False],
            correct_time=time[True],
            incorrect_time=time[False]
        )

    def get_artist_ids(self) -> List[int]:
        artist_ids = set()
        artist_ids.update(artist["artist_id"] for artist in self.correct)
        artist_ids.update(artist["artist_id"] for artist in self.incorrect)
        return list(artist_ids)

    @staticmethod
    def mean(times: List[float]) -> float:
        return 0 if len(times) == 0 else sum(times) / len(times)
