from enum import Enum


class QuizTourType(Enum):
    REGULAR = "regular"
    ALPHABET = "alphabet"
    STAIRS = "stairs"
    LETTER = "letter"
    MIRACLES_FIELD = "miracles_field"

    def to_rus(self) -> str:
        quiz_tour_type2rus = {
            QuizTourType.REGULAR: "классический",
            QuizTourType.ALPHABET: "алфавит",
            QuizTourType.STAIRS: "лесенка",
            QuizTourType.LETTER: "на одну букву",
            QuizTourType.MIRACLES_FIELD: "поле чудес"
        }
        return quiz_tour_type2rus[self]
