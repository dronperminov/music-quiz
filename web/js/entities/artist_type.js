function ArtistType(value) {
    this.value = value
}

ArtistType.prototype.ToRus = function(withUnknown = false) {
    return {
        "singer_male": "певец",
        "singer_female": "певица",
        "performer_male": "исполнитель",
        "performer_female": "исполнительница",
        "band": "группа",
        "project": "проект",
        "duet": "дуэт",
        "trio": "трио",
        "dj": "диджей",
        "via": "ВИА",
        "unknown": withUnknown ? "неизвестна" : ""
    }[this.value]
}

ArtistType.prototype.IsUnknown = function() {
    return this.value == "unknown"
}
