from enum import Enum
from typing import Optional


class Genre(Enum):
    ROCK = "rock"
    POP = "pop"
    HIP_HOP = "hip-hop"
    ELECTRO = "electro"
    DISCO = "disco"
    JAZZ_SOUL = "jazz-soul"

    @classmethod
    def from_yandex(cls: "Genre", yandex_genre: str) -> Optional["Genre"]:
        genre2yandex = {
            Genre.ROCK: {
                "allrock", "alternative", "alternativemetal", "amerfolk", "bard", "blackmetal", "classicmetal", "deathmetal", "doommetal", "epicmetal", "eurofolk",
                "extrememetal", "folk", "folkgenre", "folkmetal", "folkrock", "foreignbard", "gothicmetal", "hardcore", "hardrock", "indie", "industrial", "israelirock",
                "latinfolk", "local-indie", "metal", "metalcoregenre", "newage", "newwave", "numetal", "posthardcore", "postmetal", "postpunk", "postrock", "prog",
                "progmetal", "punk", "rnr", "rock", "romances", "rusbards", "rusfolk", "rusrock", "ska", "sludgemetal", "stonerrock", "thrashmetal", "turkishalternative",
                "turkishfolk", "turkishrock", "ukrrock"
            },
            Genre.HIP_HOP: {
                "foreignrap", "israelirap", "modern", "phonkgenre", "rap", "reggaeton", "rusrap", "triphopgenre", "turkishrap", "kazakhrap"
            },
            Genre.POP: {
                "arabicpop", "azerbaijanpop", "dance", "estrada", "hyperpopgenre", "israelipop", "japanesepop", "kpop", "newwave", "pop", "rusestrada", "ruspop", "shanson",
                "turkishpop", "uzbekpop", "edmgenre"
            },
            Genre.ELECTRO: {
                "ambientgenre", "bassgenre", "breakbeatgenre", "dnb", "dub", "dubstep", "electronics", "house", "idmgenre", "techno", "trance", "ukgaragegenre"
            },
            Genre.DISCO: {
                "disco"
            },
            Genre.JAZZ_SOUL: {
                "bebopgenre", "bigbands", "blues", "conjazz", "country", "experimental", "funk", "jazz", "rnb", "smoothjazz", "soul", "tradjazz", "vocaljazz"
            }
        }

        for genre, yandex_genres in genre2yandex.items():
            if yandex_genre in yandex_genres:
                return genre

        return None

    def to_rus(self) -> str:
        genre2rus = {
            Genre.ROCK: "рок",
            Genre.HIP_HOP: "хип-хоп",
            Genre.POP: "поп",
            Genre.ELECTRO: "электронная",
            Genre.DISCO: "диско",
            Genre.JAZZ_SOUL: "джаз / соул"
        }

        return genre2rus[self]

    def to_color(self) -> str:
        genre2color = {
            Genre.ROCK: "#ec6b56",
            Genre.HIP_HOP: "#ffc154",
            Genre.POP: "#47b39c",
            Genre.ELECTRO: "#d82e6b",
            Genre.DISCO: "#ffc154",
            Genre.JAZZ_SOUL: "#478bb3"
        }

        return genre2color[self]
