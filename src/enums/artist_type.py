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
            ArtistType.BAND: ["группа", "творческое объединение"],
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

    def to_title(self) -> str:
        artist_type2title = {
            ArtistType.SINGER_MALE: "певца",
            ArtistType.SINGER_FEMALE: "певицу",
            ArtistType.PERFORMER_MALE: "исполнителя",
            ArtistType.PERFORMER_FEMALE: "исполнительницу",
            ArtistType.BAND: "группу",
            ArtistType.PROJECT: "проект",
            ArtistType.DUET: "дуэт",
            ArtistType.TRIO: "трио",
            ArtistType.DJ: "диджея",
            ArtistType.VIA: "ВИА",
            ArtistType.UNKNOWN: "автора"
        }

        return artist_type2title[self]
