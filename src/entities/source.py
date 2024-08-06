import abc
from dataclasses import dataclass


@dataclass
class Source:
    name: str

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls: "Source", data: dict) -> "Source":
        if data["name"] == YandexSource.name:
            return YandexSource(yandex_id=data["yandex_id"])

        if data["name"] == HandSource.name:
            return HandSource()

        raise ValueError(f'Invalid Source name "{data["name"]}"')


# источником является Яндекс.Музыка
@dataclass
class YandexSource(Source):
    name = "yandex"
    yandex_id: str

    def __init__(self, yandex_id: str) -> None:
        self.yandex_id = yandex_id

    def to_dict(self) -> dict:
        return {"name": self.name, "yandex_id": self.yandex_id}


# источником является ручное добавление
class HandSource(Source):
    name = "hand"

    def __init__(self) -> None:
        pass

    def to_dict(self) -> dict:
        return {"name": self.name}
