function ArtistType(value) {
    this.value = value
    this.options = {
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
        "unknown": "неизвестна"
    }
}

ArtistType.prototype.ToRus = function() {
    return this.options[this.value]
}

ArtistType.prototype.IsUnknown = function() {
    return this.value == "unknown"
}
