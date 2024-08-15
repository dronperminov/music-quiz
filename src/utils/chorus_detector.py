import re
from typing import List, Tuple

from src.entities.lyrics_line import LyricsLine


class ChorusDetector:
    min_chorus_length: int = 2

    def detect(self, lines: List[LyricsLine]) -> List[Tuple[int, int]]:
        indices = [i for i, line in enumerate(lines) if not line.is_parenthesis()]
        lines = [line.preprocess() for line in lines]

        similarity = self.__get_similarity_matrix(indices, lines)
        chorus_start, chorus_length = self.__detect_max_chorus(indices, similarity)

        if chorus_length < self.min_chorus_length or chorus_length == len(indices):
            return []

        if chorus_length >= self.min_chorus_length * 2:
            chorus = self.detect([lines[indices[chorus_start + i]] for i in range(chorus_length)])
            if chorus and self.__is_repeated_chorus(chorus, chorus_length):
                start, end = chorus[0]
                chorus_length = end - start + 1

        return self.__get_all_choruses(indices, similarity, chorus_start, chorus_length)

    def __get_similarity_matrix(self, indices: List[int], lines: List[LyricsLine]) -> List[List[bool]]:
        similarity = [[True for _ in range(len(indices))] for _ in range(len(indices))]

        for i in range(len(indices)):
            for j in range(i):
                similarity[i][j] = lines[indices[i]].is_similar(lines[indices[j]])
                similarity[j][i] = similarity[i][j]

        return similarity

    def __detect_max_chorus(self, indices: List[int], similarity: List[List[bool]]) -> Tuple[int, int]:
        chorus_start, chorus_length = 0, 0

        for i in range(1, len(indices)):
            diagonal = "".join("1" if similarity[j + i][j] else " " for j in range(len(indices) - i))

            for match in re.finditer(r"1+", diagonal):
                start, end = match.span()
                if end - start > chorus_length:
                    chorus_start, chorus_length = start + i, end - start

        return chorus_start, chorus_length

    def __is_repeated_chorus(self, chorus: List[Tuple[int, int]], chorus_length: int) -> bool:
        if chorus[0][0] != 0 or chorus[-1][1] != chorus_length - 1:
            return False

        for i, (start, _) in enumerate(chorus[1:]):
            if start != chorus[i][1] + 1:
                return False

        return True

    def __get_all_choruses(self, indices: List[int], similarity: List[List[bool]], chorus_start: int, chorus_length: int) -> List[Tuple[int, int]]:
        chorus = []
        start = 0

        while start <= len(indices) - chorus_length:
            is_similar = all([similarity[chorus_start + i][start + i] for i in range(chorus_length)])

            if is_similar:
                chorus.append((indices[start], indices[start + chorus_length - 1]))
                start += chorus_length
            else:
                start += 1

        return chorus
