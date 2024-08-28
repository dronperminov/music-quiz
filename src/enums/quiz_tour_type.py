from enum import Enum


class QuizTourType(Enum):
    REGULAR = "regular"
    ALPHABET = "alphabet"
    STAIRS = "stairs"

    def to_rus(self) -> str:
        quiz_tour_type2rus = {
            QuizTourType.REGULAR: "Классический",
            QuizTourType.ALPHABET: "Алфавит",
            QuizTourType.STAIRS: "Лесенка"
        }
        return quiz_tour_type2rus[self]
