function Genre(value) {
    this.value = value
    this.options = {
        "rock": "рок",
        "hip-hop": "хип-хоп",
        "pop": "поп",
        "electro": "электронная",
        "disco": "диско",
        "jazz-soul": "джаз / соул"
    }
}

Genre.prototype.ToRus = function() {
    return this.options[this.value]
}

function GenreList(genres) {
    this.genres = genres.map(genre => new Genre(genre))
    this.options = {
        "rock": "рок",
        "hip-hop": "хип-хоп",
        "pop": "поп",
        "electro": "электронная",
        "disco": "диско",
        "jazz-soul": "джаз / соул"
    }
}

GenreList.prototype.ToRus = function() {
    if (this.IsEmpty())
        return "неизвестны"

    return this.genres.map(genre => genre.ToRus()).join(", ")
}

GenreList.prototype.IsEmpty = function() {
    return this.genres.length == 0
}
