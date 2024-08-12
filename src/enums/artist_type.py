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

    def to_rus(self) -> str:
        artist_type2rus = {
            ArtistType.SINGER_MALE: "певец",
            ArtistType.SINGER_FEMALE: "певица",
            ArtistType.PERFORMER_MALE: "исполнитель",
            ArtistType.PERFORMER_FEMALE: "исполнительница",
            ArtistType.BAND: "группа",
            ArtistType.PROJECT: "проект",
            ArtistType.DUET: "дуэт",
            ArtistType.TRIO: "трио",
            ArtistType.DJ: "ди-джей",
            ArtistType.VIA: "ВИА",
            ArtistType.UNKNOWN: ""
        }

        return artist_type2rus[self]
