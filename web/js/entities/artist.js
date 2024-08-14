function Artist(data) {
    this.artistId = data.artist_id
    this.source = data.source
    this.name = data.name
    this.description = data.description
    this.artistType = data.artist_type
    this.imageUrls = data.image_urls
    this.listenCount = data.listen_count
    this.tracks = data.tracks
    this.tracksCount = data.tracksCount
    this.genres = data.genres
    this.metadata = data.metadata
}

Artist.prototype.Build = function() {
    let artist = MakeElement("artist")
    let artistImage = MakeElement("artist-image", artist)
    let artistImageLink = MakeElement("", artistImage, {href: `/artists/${this.artistId}`}, "a")
    let artistImageImg = MakeElement("", artistImageLink, {src: `${this.imageUrls.length > 0 ? this.imageUrls[0] : '/images/artists/default.png'}`, loading: "lazy"}, "img")

    let artistInfo = MakeElement("artist-info", artist)

    let artistName = MakeElement("artist-name", artistInfo)
    let artistNameLink = MakeElement("", artistName, {href: `/artists/${this.artistId}`, innerText: this.name}, "a")

    let artistStats = MakeElement("artist-stats", artistInfo, {innerText: this.GetStats()})
    let artistType = MakeElement("artist-type", artistInfo, {innerText: this.ArtistTypeToRus()})
    let artistControls = MakeElement("artist-controls", artistInfo)
    let div = MakeElement("", artistControls)
    let link = MakeElement("artist-button", div, {href: `/artists/${this.artistId}`, innerText: "Смотреть"}, "a")

    return artist
}

Artist.prototype.FormatListenCount = function() {
    if (this.listenCount >= 1000000)
        return `${Round(this.listenCount / 1000000)}M`

    if (this.listenCount >= 1000)
        return `${Round(this.listenCount / 1000)}K`

    return `${this.listenCount}`
}

Artist.prototype.GetStats = function() {
    return `${this.FormatListenCount()} прослушиваний | ${GetWordForm(Object.keys(this.tracks).length, ['трек', 'трека', 'треков'])}`
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
