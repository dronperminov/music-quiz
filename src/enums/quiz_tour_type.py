from enum import Enum


class QuizTourType(Enum):
    REGULAR = "regular"
    ALPHABET = "alphabet"
    STAIRS = "stairs"
    LETTER = "letter"

    def to_rus(self) -> str:
        quiz_tour_type2rus = {
            QuizTourType.REGULAR: "Классический",
            QuizTourType.ALPHABET: "Алфавит",
            QuizTourType.STAIRS: "Лесенка",
            QuizTourType.LETTER: "На одну букву"
        }
        return quiz_tour_type2rus[self]
