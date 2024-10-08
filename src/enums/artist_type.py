import re
from enum import Enum


class ArtistType(Enum):
    UNKNOWN = "unknown"
    SINGER_MALE = "singer_male"
    SINGER_FEMALE = "singer_female"
    PERFORMER_MALE = "performer_male"
    PERFORMER_FEMALE = "performer_female"
    BAND = "band"
    PROJECT = "project"
    DUET = "duet"
    TRIO = "trio"
    DJ = "dj"
    VIA = "via"

    @classmethod
    def from_description(cls: "ArtistType", description: str) -> "ArtistType":
        artist_type2variant = {
            ArtistType.SINGER_MALE: ["певец"],
            ArtistType.SINGER_FEMALE: ["певица"],
            ArtistType.PERFORMER_MALE: ["исполнитель", "рэпер", "музыкант", "композитор"],
            ArtistType.PERFORMER_FEMALE: ["исполнительница", "рэперша"],
            ArtistType.BAND: ["группа", "творческое объединение", "бэнд", "band"],
            ArtistType.PROJECT: ["проект"],
            ArtistType.DUET: ["дуэт"],
            ArtistType.TRIO: ["трио"],
            ArtistType.DJ: ["диджей", "ди-джей", "dj"],
            ArtistType.VIA: ["вокально-инструментальный ансамбль", "виа"]
        }

        variant2artist_type = {}
        variants = []

        for artist_type, artist_type_variants in artist_type2variant.items():
            variants.extend(artist_type_variants)

            for variant in artist_type_variants:
                variant2artist_type[variant] = artist_type

        description = description.replace("\n", " ").lower()
        matched_variants = re.findall(rf'\b({"|".join(variants)})\b', description)
        return variant2artist_type[matched_variants[0]] if len(matched_variants) > 0 else ArtistType.UNKNOWN

    def to_rus(self, with_unknown: bool = False) -> str:
        artist_type2rus = {
            ArtistType.SINGER_MALE: "певец",
            ArtistType.SINGER_FEMALE: "певица",
            ArtistType.PERFORMER_MALE: "исполнитель",
            ArtistType.PERFORMER_FEMALE: "исполнительница",
            ArtistType.BAND: "группа",
            ArtistType.PROJECT: "проект",
            ArtistType.DUET: "дуэт",
            ArtistType.TRIO: "трио",
            ArtistType.DJ: "диджей",
            ArtistType.VIA: "ВИА",
            ArtistType.UNKNOWN: "неизвестна" if with_unknown else ""
        }

        return artist_type2rus[self]

    def to_title(self, simple: bool = False) -> str:
        artist_type2title = {
            ArtistType.SINGER_MALE: "исполнителя" if simple else "певца",
            ArtistType.SINGER_FEMALE: "исполнительницу" if simple else "певицу",
            ArtistType.PERFORMER_MALE: "исполнителя",
            ArtistType.PERFORMER_FEMALE: "исполнительницу",
            ArtistType.BAND: "группу",
            ArtistType.PROJECT: "группу" if simple else "проект",
            ArtistType.DUET: "группу" if simple else "дуэт",
            ArtistType.TRIO: "группу" if simple else "трио",
            ArtistType.DJ: "диджея",
            ArtistType.VIA: "ВИА",
            ArtistType.UNKNOWN: "автора"
        }

        return artist_type2title[self]

    def to_pair_title(self, simple: bool = False) -> str:
        artist_type2title = {
            ArtistType.SINGER_MALE: "обоих исполнителей" if simple else "обоих певцов",
            ArtistType.SINGER_FEMALE: "обеих исполнительниц" if simple else "обеих певиц",
            ArtistType.PERFORMER_MALE: "обоих исполнителей",
            ArtistType.PERFORMER_FEMALE: "обеих исполнительниц",
            ArtistType.BAND: "обе группы",
            ArtistType.PROJECT: "обе группы" if simple else "оба проекта",
            ArtistType.DUET: "обе группы" if simple else "оба дуэта",
            ArtistType.TRIO: "обе группы" if simple else "оба трио",
            ArtistType.DJ: "обоих диджеев",
            ArtistType.VIA: "обоих ВИА",
            ArtistType.UNKNOWN: "обоих авторов"
        }

        return artist_type2title[self]
