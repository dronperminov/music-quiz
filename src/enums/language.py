from enum import Enum


class Language(Enum):
    UNKNOWN = "unknown"
    RUSSIAN = "russian"
    FOREIGN = "foreign"

    def to_rus(self) -> str:
        language2rus = {
            Language.UNKNOWN: "",
            Language.RUSSIAN: "русский",
            Language.FOREIGN: "зарубежный"
        }

        return language2rus[self]

    def to_artists_filter(self) -> str:
        language2rus = {
            Language.UNKNOWN: "неизвестно",
            Language.RUSSIAN: "русское",
            Language.FOREIGN: "зарубежное"
        }

        return language2rus[self]
