function Track(data) {
    this.trackId = data.track_id
    this.source = data.source
    this.title = data.title
    this.artists = data.artists
    this.year = data.year
    this.lyrics = data.lyrics
    this.genres = new GenreList(data.genres)
    this.language = new Language(data.language)
    this.duration = data.duration
    this.imageUrl = data.image_url !== null ? data.image_url : '/images/tracks/default.png'
    this.metadata = new Metadata(data.metadata, "Добавлен", "Обновлён")
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

    let yearBlock = MakeElement("info-line", info)
    this.BuildYear(yearBlock)

    if (artists !== null)
        MakeElement("info-line", info, {innerHTML: this.GetArtistPositions(artists)})

    if (this.duration > 0)
        MakeElement("info-line", info, {innerHTML: `<b>Длительность:</b> ${this.FormatDuration()}`})

    let genresBlock = MakeElement("info-line", info)
    this.BuildGenres(genresBlock)

    let languageblock = MakeElement("info-line", info)
    this.BuildLanguage(languageblock)

    this.metadata.BuildInfo(info)

    this.BuildLyrics(info)
    this.BuildNote(info, artists == null || artists.length > 1 ? null : artists[0].artist_id)
    this.BuildShare(info)
    this.BuildAdmin(info)

    return info
}

Track.prototype.BuildLanguage = function(block) {
    let select = this.language.Build(block)

    let html = document.getElementsByTagName("html")[0]
    if (!html.hasAttribute("data-user-role") || html.getAttribute("data-user-role") != "admin")
        return

    select.addEventListener("change", () => {
        SendRequest("/update-track", {track_id: this.trackId, language: select.value}).then(response => {
            if (response.status != SUCCESS_STATUS) {
                ShowNotification(`Не удалось обновить язык<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
                select.value = this.language.value
                return
            }

            this.language.value = select.value
            select.classList.add("text-select")
            select.classList.remove("basic-select")
        })
    })
}

Track.prototype.BuildYear = function(block) {
    let label = MakeElement("", block, {innerHTML: `<b>Год выхода:</b> `}, "span")
    let input = MakeElement("text-input", block, {type: "text", value: this.year}, "input")

    let html = document.getElementsByTagName("html")[0]
    if (!html.hasAttribute("data-user-role") || html.getAttribute("data-user-role") != "admin") {
        input.classList.add("text-input-disabled")
        return
    }

    input.addEventListener("click", () => {
        input.classList.remove("text-input")
        input.classList.add("basic-input")
        input.classList.add("basic-input-inline")
        input.select()
    })

    label.addEventListener("click", () => {
        input.value = this.year
        input.classList.remove("basic-input")
        input.classList.remove("basic-input-inline")
        input.classList.add("text-input")
    })

    input.addEventListener("change", () => {
        let year = input.value

        if (year.match(/^[12]\d\d\d$/g) === null) {
            ShowNotification(`Значение "${year}" не является валидным годом`, "error-notification", 3500)
            return
        }

        SendRequest("/update-track", {track_id: this.trackId, year: +year}).then(response => {
            if (response.status != SUCCESS_STATUS) {
                ShowNotification(`Не удалось обновить год выхода<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
                input.value = `${this.year}`
                return
            }

            this.year = +year
            input.classList.add("text-input")
            input.classList.remove("basic-input")
        })
    })
}

Track.prototype.BuildGenres = function(block) {
    MakeElement("", block, {innerHTML: `<b>Жанры:</b> ${this.genres.ToRus()}`}, "span")
}

Track.prototype.BuildLyrics = function(block) {
    if (this.lyrics === null)
        return

    let detailsBlock = MakeElement("info-line", block)
    let details = MakeElement("details", detailsBlock)
    let detailsHeader = MakeElement("details-header", details)
    detailsHeader.addEventListener("click", () => details.classList.toggle('details-open'))

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

Track.prototype.BuildNote = function(block, artistId) {
    if (artistId === null)
        return

    let audio = document.getElementById(`audio-${this.trackId}`)
    let haveNote = audio.hasAttribute("data-note-seek")

    let noteBlock = MakeElement("info-line", block)
    let addNoteButton = MakeElement("basic-button gradient-button hidden", noteBlock, {innerText: "Добавить в заметки"}, "button")
    let removeNoteButton = MakeElement("basic-button gradient-button hidden", noteBlock, {innerText: "Удалить из заметок"}, "button")

    if (haveNote)
        removeNoteButton.classList.remove("hidden")
    else
        addNoteButton.classList.remove("hidden")

    addNoteButton.addEventListener("click", () => this.UpdateNote([addNoteButton, removeNoteButton], artistId))
    removeNoteButton.addEventListener("click", () => this.UpdateNote([addNoteButton, removeNoteButton], artistId))
}

Track.prototype.BuildShare = function(block) {
    MakeElement("info-line", block, {innerHTML: "<br><b>Поделиться треком</b>"})

    let asUnknownBlock = MakeElement("info-checkbox-line", block)
    let asUnknownInput = MakeCheckbox(asUnknownBlock, `as-unknown-${this.trackId}`, false)
    let asUnknownLabel = MakeElement("", asUnknownBlock, {innerText: "Без информации", "for": `as-unknown-${this.trackId}`}, "label")

    let fromCurrentBlock = MakeElement("info-checkbox-line", block)
    let fromCurrentInput = MakeCheckbox(fromCurrentBlock, `from-current-time-${this.trackId}`, true)
    let fromCurrentLabel = MakeElement("", fromCurrentBlock, {innerText: "С текущего места", "for": `from-current-time-${this.trackId}`}, "label")

    let shareBlock = MakeElement("info-line", block)
    let shareButton = MakeElement("basic-button gradient-button", shareBlock, {innerText: "Поделиться"}, "button")
    shareButton.addEventListener("click", async () => {
        let params = []

        if (asUnknownInput.checked)
            params.push("as_unknown=true")

        if (fromCurrentInput.checked) {
            let audio = document.getElementById(`audio-${this.trackId}`)
            params.push(`seek=${audio.currentTime}`)
        }

        let query = params.length > 0 ? `?${params.join("&")}` : ""
        await navigator.share({
            title: asUnknownInput.checked ? "Неизвестный трек" : `Трек ${this.title}`,
            text: asUnknownInput.checked ? "Угадай, что за трек:" : "Лови трек:",
            url: `https://music-quiz.plush-anvil.ru/tracks/${this.trackId}${query}`
        })
    })
}

Track.prototype.BuildAdmin = function(block) {
    let adminBlock = MakeElement("admin-buttons admin-block", block)

    let historyButton = MakeElement("basic-button gradient-button", adminBlock, {innerText: "История изменений"}, "button")
    historyButton.addEventListener("click", () => ShowHistory(`/track-history/${this.trackId}`))

    let removeButton = MakeElement("basic-button red-button", adminBlock, {innerText: "Удалить трек"}, "button")
    removeButton.addEventListener("click", () => this.Remove([removeButton]))
}

Track.prototype.FormatDuration = function() {
    let duration = Math.round(this.duration)
    let minutes = `${Math.floor(duration / 60)}`.padStart(2, '0')
    let seconds = `${duration % 60}`.padStart(2, '0')

    return `${minutes}:${seconds}`
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

Track.prototype.Remove = function(buttons) {
    if (!confirm(`Вы уверены, что хотите удалить трек "${this.title}"?`))
        return

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/remove-track", {track_id: this.trackId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            for (let button of buttons)
                button.removeAttribute("disabled")

            ShowNotification(`Не удалось удалить трек "${this.title}".<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        location.reload()
    })
}

Track.prototype.UpdateNote = function(buttons, artistId) {
    let audio = document.getElementById(`audio-${this.trackId}`)
    let seek = audio.currentTime

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/update-note", {artist_id: artistId, track: {track_id: this.trackId, seek: seek}}).then(response => {
        for (let button of buttons)
            button.removeAttribute("disabled")

        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось обновить заметку.<br><b>Причина</b>: ${response.message}`, "error-notification", 3500)
            return
        }

        ShowNotification(`Заметка успешно обновлена`, "success-notification", 3500)

        for (let button of buttons)
            button.classList.toggle("hidden")

        if (audio.hasAttribute("data-note-seek"))
            audio.removeAttribute("data-note-seek")
        else
            audio.setAttribute("data-note-seek", seek)
    })
}

Track.prototype.ReplaceUnknown = function(artists) {
    let menu = document.getElementById("track-menu")
    menu.removeAttribute("disabled")

    let image = document.getElementById("track-image")
    image.setAttribute("src", this.imageUrl)

    let circle = document.getElementById("track-circle")
    if (circle !== null)
        circle.classList.remove("hidden")

    let title = document.getElementById("track-title")
    title.innerText = this.title

    let year = document.getElementById("track-year")
    year.innerText = this.year

    let artistNames = []
    for (let artist of artists) {
        let link = document.getElementById(`link-artist-${artist.artist_id}`)
        link.setAttribute("href", `/artists/${artist.artist_id}`)
        link.innerText = artist.name
        artistNames.push(artist.name)
    }

    let query = `${artistNames.join(" ")} ${this.title} год выхода`
    year.href = `https://www.google.com/search?q=${encodeURIComponent(query)}`

    SetMediaSessionMetadata(this.trackId)
}
