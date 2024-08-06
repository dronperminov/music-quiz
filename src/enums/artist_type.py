from enum import Enum


class ArtistType(Enum):
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
