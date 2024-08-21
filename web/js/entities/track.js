function Track(data) {
    this.trackId = data.track_id
    this.source = data.source
    this.title = data.title
    this.artists = data.artists
    this.year = data.year
    this.lyrics = data.lyrics
    this.genres = data.genres
    this.language = data.language
    this.duration = data.duration
    this.imageUrl = data.image_url !== null ? data.image_url : '/images/tracks/default.png'
    this.metadata = data.metadata
}

Track.prototype.BuildInfo = function(artists = null) {
    let info = MakeElement("info")
    info.setAttribute("id", `info-track-${this.trackId}`)

    let closeIcon = MakeElement("close-icon", info, {title: "Закрыть"})

    let infoImage = MakeElement("info-image", info)
    let img = MakeElement("", infoImage, {src: this.imageUrl, loading: "lazy"}, "img")

    if (this.source.name == "yandex") {
        let header = MakeElement("info-header-line", info)
        let link = MakeElement("", header, {href: `https://music.yandex.ru/track/${this.source.yandex_id}`, target: "_blank"}, "a")
        let img = MakeElement("", link, {src: "/images/ya_music.svg"}, "img")
        let span = MakeElement("", header, {innerText: this.title}, "span")
    }
    else {
        MakeElement("info-header-line", info, {innerHTML: this.title})
    }

    if (this.year > 0)
        MakeElement("info-line", info, {innerHTML: `<b>Год выхода:</b> ${this.year}`})

    if (artists !== null)
        MakeElement("info-line", info, {innerHTML: this.GetArtistPositions(artists)})

    if (this.duration > 0)
        MakeElement("info-line", info, {innerHTML: `<b>Длительность:</b> ${this.FormatDuration()}`})

    if (this.genres.length > 0)
        MakeElement("info-line", info, {innerHTML: `<b>Жанры:</b> ${this.genres.map(genre => this.GenreToRus(genre)).join(", ")}`})

    if (this.language != "unknown")
        MakeElement("info-line", info, {innerHTML: `<b>Язык:</b> ${this.LanguageToRus(this.language)}`})

    MakeElement("info-line", info, {innerHTML: `<b>Добавлен:</b> ${this.FormatMetadataDate(this.metadata.created_at)} пользователем @${this.metadata.created_by}`})

    if (this.metadata.created_at != this.metadata.updated_at)
        MakeElement("info-line", info, {innerHTML: `<b>Обновлён:</b> ${this.FormatMetadataDate(this.metadata.updated_at)} пользователем @${this.metadata.updated_by}`})

    let history = MakeElement("info-line", info)
    let historyLink = MakeElement("link", history, {href: "#", innerText: "История изменений"}, "a")
    history.addEventListener("click", () => ShowHistory(`/track-history/${this.trackId}`))

    if (this.lyrics !== null) {
        let details = MakeElement("details details-open", info)
        let detailsHeader = MakeElement("details-header", details)
        MakeElement("details-icon", detailsHeader, {}, "span")
        MakeElement("", detailsHeader, {innerText: " Текст"}, "span")

        let detailsContent = MakeElement("details-content", details)
        let lyrics = MakeElement("track-lyrics", detailsContent)
        let indices = this.GetChorusIndices()

        for (let i = 0; i < this.lyrics.lines.length; i++) {
            let line = MakeElement("track-lyrics-line", lyrics, {innerText: this.lyrics.lines[i].text})

            if (i in indices)
                line.classList.add("track-lyrics-line-chorus")

            let index1 = `${i}` in indices ? indices[`${i}`] : -1
            let index2 = `${i + 1}` in indices ? indices[`${i + 1}`] : -1

            if (index1 != index2)
                MakeElement("", lyrics, {}, "br")
        }
    }

    return info
}

Track.prototype.FormatMetadataDate = function(datetime) {
    let {date, time} = ParseDateTime(datetime)
    return `${date} в ${time}`
}

Track.prototype.FormatDuration = function() {
    let duration = Math.round(this.duration)
    let minutes = `${Math.floor(duration / 60)}`.padStart(2, '0')
    let seconds = `${duration % 60}`.padStart(2, '0')

    return `${minutes}:${seconds}`
}

Track.prototype.GenreToRus = function(genre) {
    return {
        "rock": "рок",
        "hip-hop": "хип-хоп",
        "pop": "поп",
        "electro": "электронная",
        "disco": "диско",
        "jazz-soul": "джаз / соул"
    }[genre]
}

Track.prototype.LanguageToRus = function(language) {
    return {
        "unknown": "",
        "russian": "русский",
        "foreign": "зарубежный"
    }[language]
}

Track.prototype.GetChorusIndices = function() {
    let indices = {}

    for (let i = 0; i < this.lyrics.chorus.length; i++)
        for (let index = this.lyrics.chorus[i][0]; index <= this.lyrics.chorus[i][1]; index++)
            indices[`${index}`] = i

    return indices
}

Track.prototype.GetArtistPositions = function(artists) {
    if (artists === null)
        return ""

    if (artists.length == 1)
        return `<b>Позиция у исполнителя:</b> ${artists[0].tracks[this.trackId]}`

    let positions = artists.map(artist => `<li>${artist.name}: ${artist.tracks[this.trackId]}</li>`).join("")
    return `<b>Позиции у исполнителей:</b> <ul>${positions}</ul>`
}
