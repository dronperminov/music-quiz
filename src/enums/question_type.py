from enum import Enum


class QuestionType(Enum):
    ARTIST_BY_TRACK = "artist_by_track"
    ARTIST_BY_INTRO = "artist_by_intro"
    LINE_BY_TEXT = "line_by_text"
    LINE_BY_CHORUS = "line_by_chorus"
    NAME_BY_TRACK = "name_by_track"

    def to_rus(self) -> str:
        question_type2rus = {
            QuestionType.ARTIST_BY_TRACK: "исполнитель по треку",
            QuestionType.ARTIST_BY_INTRO: "исполнитель по вступлению",
            QuestionType.LINE_BY_TEXT: "строка по тексту",
            QuestionType.LINE_BY_CHORUS: "строка по припеву",
            QuestionType.NAME_BY_TRACK: "название по треку"
        }

        return question_type2rus[self]
