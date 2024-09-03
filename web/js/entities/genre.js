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

GenreList.prototype.Set = function(genres) {
    this.genres = genres.map(genre => new Genre(genre))
}

GenreList.prototype.Get = function() {
    return this.genres.map(genre => genre.value)
}

GenreList.prototype.ToRus = function() {
    if (this.IsEmpty())
        return "неизвестны"

    return this.genres.map(genre => genre.ToRus()).join(", ")
}

GenreList.prototype.IsEmpty = function() {
    return this.genres.length == 0
}

GenreList.prototype.Build = function(parent) {
    let label = MakeElement("", parent, {innerHTML: `<b>Жанры:</b> `}, "span")
    let span = MakeElement("", parent, {innerText: this.ToRus()}, "span")

    let select = MakeMultiSelect(parent, this.options, [])
    let input = new MultiSelect(select, null, true)

    select.classList.add("hidden")

    label.addEventListener("click", () => {
        select.classList.toggle("hidden")
        input.SetSelected(this.genres.map(genre => genre.value))
        span.classList.toggle("hidden")
        span.innerText = this.ToRus()
    })

    return input
}
