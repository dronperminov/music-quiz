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
    this.metadata = new Metadata(data.metadata, "Добавлен", "Обновлён")
}

Artist.prototype.Build = function(artistId2scale = null) {
    let artist = MakeElement("artist")
    let artistImage = MakeElement("artist-image", artist)
    let artistImageLink = MakeElement("", artistImage, {href: `/artists/${this.artistId}`}, "a")
    let artistImageImg = MakeElement("", artistImageLink, {src: this.imageUrls[0], loading: "lazy"}, "img")

    let artistInfo = MakeElement("artist-data", artist)

    let artistName = MakeElement("artist-name", artistInfo)

    this.BuildScale(artistName, artistId2scale)

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

    this.metadata.BuildInfo(info)

    this.BuildAdmin(info)

    return info
}

Artist.prototype.BuildPage = function(artistId2scale, note, blockId = "artist") {
    let artist = document.getElementById(blockId)

    let artistImage = MakeElement("artist-image", artist)
    let artistImageImg = MakeElement("", artistImage, {src: this.imageUrls[0], loading: "lazy"}, "img")

    let artistName = MakeElement("artist-name", artist)

    if (this.source.name == "yandex") {
        let link = MakeElement("", artistName, {href: `https://music.yandex.ru/artist/${this.source.yandex_id}`, target: "_blank"}, "a")
        let img = MakeElement("", link, {src: "/images/ya_music.svg"}, "img")
    }

    let span = MakeElement("", artistName, {innerText: this.name}, "span")

    let scaleBlock = MakeElement("artist-scale", artist)
    this.BuildScale(scaleBlock, artistId2scale)

    let artistStats = MakeElement("artist-stats", artist, {innerHTML: this.GetStats()})

    this.BuildPageAbout(artist)
    this.BuildNote(artist, note)
}

Artist.prototype.BuildScale = function(block, artistId2scale) {
    if (artistId2scale === null || !(this.artistId in artistId2scale))
        return

    let scale = artistId2scale[this.artistId]
    let circle = MakeElement("circle", block, {style: `background-color: hsl(${scale.scale * 120}, 70%, 50%)`})
    let correct = GetWordForm(scale.correct, ['корректный', 'корректных', 'корректных'])
    let incorrect = GetWordForm(scale.incorrect, ['некорректный', 'некорректных', 'некорректных'])
    circle.addEventListener("click", () => ShowNotification(`<b>${this.name}</b>: ${correct} и ${incorrect}`, 'info-notification', 3000))
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
    let input = this.genres.Build(block)

    input.onChange = () => {
        let genres = input.GetSelected()

        if (genres.length == 0)
            return

        SendRequest("/update-artist", {artist_id: this.artistId, genres: genres, update_tracks: true}).then(response => {
            if (response.status != SUCCESS_STATUS) {
                ShowNotification(`Не удалось обновить жанры<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
                input.SetSelected(this.genres.Get())
                return
            }

            this.genres.Set(genres)
        })
    }
}

Artist.prototype.BuildPageAbout = function(block) {
    let detailsAbout = MakeDetails(block, "Об исполнителе")

    if (this.description.length > 0)
        MakeElement("artist-about", detailsAbout, {innerHTML: this.description})

    let artistTypeBlock = MakeElement("artist-about", detailsAbout)
    this.BuildArtistType(artistTypeBlock)

    let genresBlock = MakeElement("artist-about", detailsAbout)
    this.BuildGenres(genresBlock)

    this.metadata.BuildInfo(detailsAbout, "artist-about")
}

Artist.prototype.BuildNote = function(block, note) {
    let noteBlock = MakeElement("user-block artist-note", block)
    let noteHeader = MakeElement("artist-note-header", noteBlock, {innerText: "Личные заметки"})
    let noteTextarea = MakeElement("basic-textarea auto-resize-textarea", noteBlock, {placeholder: "Напишите здесь что-нибудь"}, "textarea")

    if (note !== null)
        noteTextarea.value = note.text

    let input = new NoteInput(noteTextarea)
    noteTextarea.addEventListener("change", () => this.UpdateNote(noteTextarea))
}

Artist.prototype.BuildAdmin = function(block) {
    let adminBlock = MakeElement("admin-buttons admin-block", block)
    let buttons = []

    let historyButton = MakeElement("basic-button gradient-button", adminBlock, {innerText: "История изменений"}, "button")
    buttons.push(historyButton)
    historyButton.addEventListener("click", () => ShowHistory(`/artist-history/${this.artistId}`))

    if (this.source.name == "yandex") {
        let button = MakeElement("basic-button gradient-button", adminBlock, {innerText: "Распарсить"}, "button")
        buttons.push(button)
        button.addEventListener("click", () => ParseArtists(buttons, [this.source.yandex_id]))
    }

    let removeButton = MakeElement("basic-button red-button", adminBlock, {innerText: "Удалить исполнителя"}, "button")
    buttons.push(removeButton)

    let markupButton = MakeElement("basic-button gradient-button", adminBlock, {innerText: "Разметить треки"}, "button")
    buttons.push(markupButton)

    removeButton.addEventListener("click", () => this.Remove(buttons))
    markupButton.addEventListener("click", () => location.href = `/markup-track?artist_id=${this.artistId}`)
}

Artist.prototype.FormatListenCount = function() {
    if (this.listenCount >= 1000000)
        return `${Round(this.listenCount / 1000000)}M`

    if (this.listenCount >= 1000)
        return `${Round(this.listenCount / 1000)}K`

    return `${this.listenCount}`
}

Artist.prototype.GetStats = function() {
    let listenCount = this.listenCount < 1000 ? GetWordForm(this.listenCount, ['слушатель', 'слушателя', 'слушателей']) : `${this.FormatListenCount()} слушателей`
    let tracksCount = `${GetWordForm(Object.keys(this.tracks).length, ['трек', 'трека', 'треков'])} из ${this.tracksCount}`
    let stats = [listenCount, tracksCount]

    if (!this.artistType.IsUnknown())
        stats.push(this.artistType.ToRus())

    stats.push(this.genres.ToRus())
    return stats.join(" | ")
}

Artist.prototype.Remove = function(buttons) {
    if (!confirm(`Вы уверены, что хотите удалить исполнителя "${this.name}" и все его треки?`))
        return

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/remove-artist", {artist_id: this.artistId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            for (let button of buttons)
                button.removeAttribute("disabled")

            ShowNotification(`Не удалось удалить исполнителя "${this.name}".<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        location.reload()
    })
}

Artist.prototype.UpdateNote = function(textarea) {
    let text = textarea.value.trim()
    textarea.value = text

    SendRequest("/update-note", {text: text, artist_id: this.artistId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось обновить текст заметки исполнителя "${this.name}".<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
        }
        else {
            ShowNotification(`Текст заметки исполнителя "${this.name}" успешно обновлён`, "success-notification", 3500)
        }
    })
}
