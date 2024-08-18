function Artist(data) {
    this.artistId = data.artist_id
    this.source = data.source
    this.name = data.name
    this.description = data.description
    this.artistType = data.artist_type
    this.imageUrls = data.image_urls.length > 0 ? data.image_urls : ['/images/artists/default.png']
    this.listenCount = data.listen_count
    this.tracks = data.tracks
    this.tracksCount = data.tracks_count
    this.genres = data.genres
    this.metadata = data.metadata
}

Artist.prototype.Build = function() {
    let artist = MakeElement("artist")
    let artistImage = MakeElement("artist-image", artist)
    let artistImageLink = MakeElement("", artistImage, {href: `/artists/${this.artistId}`}, "a")
    let artistImageImg = MakeElement("", artistImageLink, {src: this.imageUrls[0], loading: "lazy"}, "img")

    let artistInfo = MakeElement("", artist)

    let artistName = MakeElement("artist-name", artistInfo)
    let artistNameLink = MakeElement("", artistName, {href: `/artists/${this.artistId}`, innerText: this.name}, "a")

    let artistStats = MakeElement("artist-stats", artistInfo, {innerText: this.GetStats()})
    let artistType = MakeElement("artist-type", artistInfo, {innerText: this.ArtistTypeToRus()})
    let artistControls = MakeElement("artist-controls", artistInfo)
    let div = MakeElement("", artistControls)
    let link = MakeElement("gradient-button", div, {href: `/artists/${this.artistId}`, innerText: "Смотреть"}, "a")

    let artistMenu = MakeElement("artist-menu", artist)
    let verticalHam = MakeElement("vertical-ham", artistMenu, {innerHTML: "<div></div><div></div><div></div>"})
    verticalHam.addEventListener("click", () => infos.Show(`artist-${this.artistId}`))

    return artist
}

Artist.prototype.BuildInfo = function() {
    let info = MakeElement("info")
    info.setAttribute("id", `info-artist-${this.artistId}`)

    let closeIcon = MakeElement("close-icon", info, {title: "Закрыть"})
    let infoImages = MakeElement("info-images", info)
    let infoImagesDiv = MakeElement("", infoImages)

    for (let imageUrl of this.imageUrls) {
        let infoImage = MakeElement("info-image", infoImagesDiv)
        let img = MakeElement("", infoImage, {src: imageUrl, loading: "lazy"}, "img")
    }

    if (this.source.name == "yandex") {
        let header = MakeElement("info-header-line", info)
        let link = MakeElement("", header, {href: `https://music.yandex.ru/artist/${this.source.yandex_id}`, target: "_blank"}, "a")
        let img = MakeElement("", link, {src: "/images/ya_music.svg"}, "img")
        let span = MakeElement("", header, {innerText: this.name}, "span")
    }
    else {
        MakeElement("info-header-line", info, {innerHTML: this.name})
    }

    if (this.description.length > 0)
        MakeElement("info-description-line", info, {innerHTML: this.description})

    if (this.genres.length > 0)
        MakeElement("info-line", info, {innerHTML: `<b>Жанры:</b> ${this.genres.map(genre => this.GenreToRus(genre)).join(", ")}`})

    MakeElement("info-line", info, {innerHTML: `<b>Треков:</b> ${Object.keys(this.tracks).length} из ${this.tracksCount}`})
    MakeElement("info-line", info, {innerHTML: `<b>Добавлен:</b> ${this.FormatMetadataDate(this.metadata.created_at)} пользователем @${this.metadata.created_by}`})

    if (this.metadata.created_at != this.metadata.updated_at)
        MakeElement("info-line", info, {innerHTML: `<b>Обновлён:</b> ${this.FormatMetadataDate(this.metadata.updated_at)} пользователем @${this.metadata.updated_by}`})

    return info
}

Artist.prototype.FormatListenCount = function() {
    if (this.listenCount >= 1000000)
        return `${Round(this.listenCount / 1000000)}M`

    if (this.listenCount >= 1000)
        return `${Round(this.listenCount / 1000)}K`

    return `${this.listenCount}`
}

Artist.prototype.FormatMetadataDate = function(date) {
    let match = (/^(?<year>\d\d\d\d)-(?<month>\d\d?)-(?<day>\d\d?)T(?<time>\d\d?:\d\d:\d\d?)$/g).exec(date)
    let groups = match.groups

    return `${groups.day}.${groups.month}.${groups.year} в ${groups.time}`
}

Artist.prototype.GetStats = function() {
    let listenCount = this.listenCount < 1000 ? GetWordForm(this.listenCount, ['слушатель', 'слушателя', 'слушателей']) : `${this.FormatListenCount()} слушателей`
    let tracksCount = `${GetWordForm(Object.keys(this.tracks).length, ['трек', 'трека', 'треков'])} из ${this.tracksCount}`
    return [listenCount, tracksCount].join(" | ")
}

Artist.prototype.ArtistTypeToRus = function() {
    return {
        "singer_male": "певец",
        "singer_female": "певица",
        "performer_male": "исполнитель",
        "performer_female": "исполнительница",
        "band": "группа",
        "project": "проект",
        "duet": "дуэт",
        "trio": "трио",
        "dj": "ди-джей",
        "via": "ВИА",
        "unknown": ""
    }[this.artistType]
}

Artist.prototype.GenreToRus = function(genre) {
    return {
        "rock": "рок",
        "hip-hop": "хип-хоп",
        "pop": "поп",
        "electro": "электронная",
        "disco": "диско",
        "jazz-soul": "джаз / соул"
    }[genre]
}
