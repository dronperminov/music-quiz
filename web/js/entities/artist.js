function Artist(data) {
    this.artistId = data.artist_id
    this.source = data.source
    this.name = data.name
    this.description = data.description
    this.artistType = new ArtistType(data.artist_type)
    this.imageUrls = data.image_urls.length > 0 ? data.image_urls : ['/images/artists/default.png']
    this.listenCount = data.listen_count
    this.tracks = data.tracks
    this.tracksCount = data.tracks_count
    this.genres = new GenreList(data.genres)
    this.metadata = data.metadata
}

Artist.prototype.Build = function(artistId2scale = null) {
    let artist = MakeElement("artist")
    let artistImage = MakeElement("artist-image", artist)
    let artistImageLink = MakeElement("", artistImage, {href: `/artists/${this.artistId}`}, "a")
    let artistImageImg = MakeElement("", artistImageLink, {src: this.imageUrls[0], loading: "lazy"}, "img")

    let artistInfo = MakeElement("artist-data", artist)

    let artistName = MakeElement("artist-name", artistInfo)

    if (artistId2scale !== null && this.artistId in artistId2scale) {
        let scale = artistId2scale[this.artistId]
        let circle = MakeElement("circle", artistName, {style: `background-color: hsl(${scale.scale * 120}, 70%, 50%)`})
        let correct = GetWordForm(scale.correct, ['корректный', 'корректных', 'корректных'])
        let incorrect = GetWordForm(scale.incorrect, ['некорректный', 'некорректных', 'некорректных'])
        circle.addEventListener("click", () => ShowNotification(`<b>${this.name}</b>: ${correct} и ${incorrect}`, 'info-notification', 3000))
    }

    let artistNameLink = MakeElement("", artistName, {href: `/artists/${this.artistId}`, innerText: this.name}, "a")

    let artistStats = MakeElement("artist-stats", artistInfo, {innerHTML: this.GetStats()})
    let artistControls = MakeElement("artist-controls", artistInfo)
    let div = MakeElement("", artistControls)
    let link = MakeElement("gradient-link", div, {href: `/artists/${this.artistId}`, innerText: "Смотреть"}, "a")

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

    let artistTypeBlock = MakeElement("info-line", info)
    this.BuildArtistType(artistTypeBlock)

    let genresBlock = MakeElement("info-line", info)
    this.BuildGenres(genresBlock)

    MakeElement("info-line", info, {innerHTML: `<b>Треков:</b> ${Object.keys(this.tracks).length} из ${this.tracksCount}`})
    MakeElement("info-line", info, {innerHTML: `<b>Добавлен:</b> ${this.FormatMetadataDate(this.metadata.created_at)} пользователем @${this.metadata.created_by}`})

    if (this.metadata.created_at != this.metadata.updated_at)
        MakeElement("info-line", info, {innerHTML: `<b>Обновлён:</b> ${this.FormatMetadataDate(this.metadata.updated_at)} пользователем @${this.metadata.updated_by}`})

    let history = MakeElement("info-line admin-block", info)
    let historyLink = MakeElement("link", history, {href: "#", innerText: "История изменений"}, "a")
    history.addEventListener("click", () => ShowHistory(`/artist-history/${this.artistId}`))

    if (this.source.name == "yandex") {
        let buttonBlock = MakeElement("info-line admin-block", info)
        let button = MakeElement("basic-button gradient-button", buttonBlock, {innerText: "Распарсить"}, "button")
        button.addEventListener("click", () => ParseArtists([button], [this.source.yandex_id]))
    }

    return info
}

Artist.prototype.BuildArtistType = function(block) {
    let select = this.artistType.Build(block)

    let html = document.getElementsByTagName("html")[0]
    if (!html.hasAttribute("data-user-role") || html.getAttribute("data-user-role") != "admin")
        return

    select.addEventListener("change", () => {
        SendRequest("/update-artist", {artist_id: this.artistId, artist_type: select.value}).then(response => {
            if (response.status != SUCCESS_STATUS) {
                ShowNotification(`Не удалось обновить форму записии<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
                select.value = this.artistType.value
                return
            }

            this.artistType.value = select.value
            select.classList.add("text-select")
            select.classList.remove("basic-select")
        })
    })
}

Artist.prototype.BuildGenres = function(block) {
    MakeElement("", block, {innerHTML: `<b>Жанры:</b> ${this.genres.ToRus()}`}, "span")
}

Artist.prototype.FormatListenCount = function() {
    if (this.listenCount >= 1000000)
        return `${Round(this.listenCount / 1000000)}M`

    if (this.listenCount >= 1000)
        return `${Round(this.listenCount / 1000)}K`

    return `${this.listenCount}`
}

Artist.prototype.FormatMetadataDate = function(datetime) {
    let {date, time} = ParseDateTime(datetime)
    return `${date} в ${time}`
}

Artist.prototype.GetStats = function() {
    let listenCount = this.listenCount < 1000 ? GetWordForm(this.listenCount, ['слушатель', 'слушателя', 'слушателей']) : `${this.FormatListenCount()} слушателей`
    let tracksCount = `${GetWordForm(Object.keys(this.tracks).length, ['трек', 'трека', 'треков'])} из ${this.tracksCount}`
    let stats = [listenCount, tracksCount]

    if (!this.artistType.IsUnknown())
        stats.push(this.artistType.ToRus())

    return stats.join(" | ")
}
