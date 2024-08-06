from enum import Enum


class QuestionType(Enum):
    ARTIST_BY_TRACK = "artist_by_track"
    ARTIST_BY_INTRO = "artist_by_intro"
    LINE_BY_TEXT = "line_by_text"
    LINE_BY_CHORUS = "line_by_chorus"
    FIRST_WORD_BY_TEXT = "first_word_by_text"
    LAST_WORD_BY_TEXT = "last_word_by_text"
    FIRST_WORD_BY_CHORUS = "first_word_by_chorus"
    LAST_WORD_BY_CHORUS = "last_word_by_chorus"
    NAME_BY_TRACK = "name_by_track"
