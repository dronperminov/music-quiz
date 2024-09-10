function GetSearchParams() {
    let listenCount = listenCountInput.GetValue()

    if (listenCount === null)
        return null

    let years = yearsInput.GetValue()

    if (years === null)
        return null

    let tracksCount = tracksCountInput.GetValue()
    if (tracksCount === null)
        return null

    let addedTracks = addedTracksInput.GetValue()
    if (addedTracks === null)
        return null

    return {
        query: document.getElementById("query").value.trim(),
        target: document.getElementById("target").value,
        order: document.getElementById("order").value,
        order_type: +document.getElementById("order-type").value,
        listen_count: listenCount,
        years: years,
        tracks_count: tracksCount,
        added_tracks: addedTracks,
        genres: genresInput.GetValue(),
        artist_type: artistTypeInput.GetValue(),
        artists_count: artistsCountInput.GetValue(),
        language: languageInput.GetValue()
    }
}

function LoadArtists(response, block) {
    for (let artist of response.artists) {
        artist = new Artist(artist)
        block.appendChild(artist.Build(response.artist_id2scale))
        infos.Add(artist.BuildInfo())
    }

    return response.artists.length
}

function PushUrlParams(params = null) {
    let url = new URL(window.location.href)

    let keys = []
    for (let [key, value] of url.searchParams.entries())
        keys.push(key)

    for (let key of keys)
        url.searchParams.delete(key)

    if (params !== null) {
        if (params.query !== "")
            url.searchParams.set("query", params.query)

        for (let key of ["target", "order", "order_type"])
            url.searchParams.set(key, params[key])

        for (let key of ["listen_count", "years", "tracks_count", "added_tracks"])
            if (params[key][0] !== "" || params[key][1] !== "")
                url.searchParams.set(key, JSON.stringify(params[key]))

        for (let key of ["genres", "artist_type", "artists_count", "language"])
            if (Object.keys(params[key]).length > 0)
                url.searchParams.set(key, JSON.stringify(params[key]))
    }

    window.history.pushState(null, '', url.toString())
}

function SearchArtists() {
    let params = GetSearchParams()
    if (params === null)
        return

    for (let shortArtists of document.getElementsByClassName("short-artists-block"))
        shortArtists.classList.add("hidden")

    PushUrlParams(params)

    search.CloseFiltersPopup()
    infiniteScroll.Reset()
    infiniteScroll.LoadContent()
}

function ClearArtists() {
    infiniteScroll.Reset()
    PushUrlParams()

    for (let shortArtists of document.getElementsByClassName("short-artists-block"))
        shortArtists.classList.remove("hidden")
}

function SearchShortArtists(order, orderType, target = "all") {
    let queryInput = document.getElementById("query")
    let targetInput = document.getElementById("target")
    let orderInput = document.getElementById("order")
    let orderTypeInput = document.getElementById("order-type")

    queryInput.value = ""
    targetInput.value = target
    orderInput.value = order
    orderTypeInput.value = orderType
    listenCountInput.Clear()
    genresInput.Clear()
    artistTypeInput.Clear()

    SearchArtists()
}

function BuildAdminInfo() {
    let info = MakeElement("info", null, {id: "info-admin"})

    MakeElement("close-icon", info, {title: "Закрыть"})
    MakeElement("info-header-line", info, {innerText: "Управление"})

    let chartBlock = MakeElement("info-line", info, {innerHTML: "<b>Чарт</b>"})
    MakeElement("description", chartBlock, {innerText: "Актуальный чарт Яндекс.Музыки, содержащий 100 популярных треков"})
    let chartButton = MakeElement("basic-button gradient-button", info, {innerText: "Обновить"}, "button")

    MakeElement("info-divider-line", info)

    let artistBlock = MakeElement("info-line", info, {innerHTML: "<b>Исполнители</b>"})
    MakeElement("description", artistBlock, {innerText: "Добавление новых и обновление имеющихся исполнителей"})

    let artistUrlBlock = MakeElement("info-textarea-line", info)
    let artistUrlLabel = MakeElement("", artistUrlBlock, {innerText: "Ссылки:", "for": "artist-url"}, "label")
    let artistUrlInput = MakeElement("basic-textarea", artistUrlBlock, {type: "text", value: "", placeholder: "https://music.yandex.ru/artist/...", id: "artist-url"}, "textarea")
    MakeElement("error", info, {id: "artist-url-error"})

    let fromPlaylistBlock = MakeElement("info-checkbox-line", info)
    let fromPlaylistInput = MakeCheckbox(fromPlaylistBlock, "artist-from-playlist", true)
    let fromPlaylistLabel = MakeElement("", fromPlaylistBlock, {innerText: "Парсить плейлист", "for": "artist-from-playlist"}, "label")

    let maxTracksBlock = MakeElement("info-input-line", info)
    let maxTracksLabel = MakeElement("", maxTracksBlock, {innerText: "Треков не более (на исполнителя):", "for": "artist-max-tracks"}, "label")
    let maxTracksInput = MakeElement("basic-input", maxTracksBlock, {type: "text", value: "20", id: "artist-max-tracks"}, "input")
    MakeElement("error", info, {id: "artist-max-tracks-error"})

    let maxArtistsBlock = MakeElement("info-input-line", info)
    let maxArtistsLabel = MakeElement("", maxArtistsBlock, {innerText: "Исполнителей трека не более:", "for": "artist-max-artists"}, "label")
    let maxArtistsInput = MakeElement("basic-input", maxArtistsBlock, {type: "text", value: "1", id: "artist-max-artists"}, "input")
    MakeElement("error", info, {id: "artist-max-artists-error"})

    let artistButton = MakeElement("basic-button gradient-button", info, {innerText: "Добавить"}, "button")

    MakeElement("info-divider-line", info)

    let trackBlock = MakeElement("info-line", info, {innerHTML: "<b>Треки</b>"})
    MakeElement("description", trackBlock, {innerText: "Добавление новых и обновление имеющихся треков"})

    let trackUrlBlock = MakeElement("info-textarea-line", info)
    let trackUrlLabel = MakeElement("", trackUrlBlock, {innerText: "Ссылки:", "for": "track-url"}, "label")
    let trackUrlInput = MakeElement("basic-textarea", trackUrlBlock, {type: "text", value: "", placeholder: "https://music.yandex.ru/track/...", id: "track-url"}, "textarea")
    MakeElement("error", info, {id: "track-url-error"})

    let trackButton = MakeElement("basic-button gradient-button", info, {innerText: "Добавить"}, "button")

    MakeElement("info-divider-line", info)

    let historyBlock = MakeElement("info-line", info, {innerHTML: "<b>История</b>"})
    MakeElement("description", historyBlock, {innerText: "История изменения базы данных"})

    let artistActionsBlock = MakeElement("info-checkbox-line", info)
    let artistActionsInput = MakeCheckbox(artistActionsBlock, "artist-actions", true)
    let artistActionsLabel = MakeElement("", artistActionsBlock, {innerText: "Действия с исполнителями", "for": "artist-actions"}, "label")

    let trackActionsBlock = MakeElement("info-checkbox-line", info)
    let trackActionsInput = MakeCheckbox(trackActionsBlock, "track-actions", true)
    let trackActionsLabel = MakeElement("", trackActionsBlock, {innerText: "Действия с треками", "for": "track-actions"}, "label")

    let artistsGroupActionsBlock = MakeElement("info-checkbox-line", info)
    let artistsGroupActionsInput = MakeCheckbox(artistsGroupActionsBlock, "artists-groups-actions", true)
    let artistsGroupActionsLabel = MakeElement("", artistsGroupActionsBlock, {innerText: "Действия с группами", "for": "artists-groups-actions"}, "label")

    let limitBlock = MakeElement("info-input-line", info)
    let limitLabel = MakeElement("", limitBlock, {innerText: "Количество записей:", "for": "history-limit"}, "label")
    let limitInput = MakeElement("basic-input", limitBlock, {type: "text", value: "100", id: "history-limit"}, "input")
    MakeElement("error", info, {id: "history-limit-error"})

    let skipBlock = MakeElement("info-input-line", info)
    let skipLabel = MakeElement("", skipBlock, {innerText: "Смещение:", "for": "history-skip"}, "label")
    let skipInput = MakeElement("basic-input", skipBlock, {type: "text", value: "0", id: "history-skip"}, "input")
    MakeElement("error", info, {id: "history-skip-error"})

    let historyButton = MakeElement("basic-button gradient-button", info, {innerText: "Получить"}, "button")

    artistUrlLabel.addEventListener("click", () => {
        artistUrlInput.value = ""
        artistUrlInput.focus()
    })

    chartButton.addEventListener("click", () => ParseChart([chartButton, artistButton, trackButton]))
    artistButton.addEventListener("click", () => AddArtist([chartButton, artistButton, trackButton]))
    trackButton.addEventListener("click", () => AddTrack([chartButton, artistButton, trackButton]))
    historyButton.addEventListener("click", () => {
        let artistActions = artistActionsInput.checked ? ["add_artist", "edit_artist", "remove_artist"] : []
        let trackActions = trackActionsInput.checked ? ["add_track", "edit_track", "remove_track"] : []
        let artistsGroupActions = artistsGroupActionsInput.checked ? ["add_artists_group", "edit_artists_group", "remove_artists_group"] : []
        let limitInput = new NumberInput("history-limit", 1, Infinity, /^\d+$/g)
        let limit = limitInput.GetValue()

        if (limit === null)
            return

        let skipInput = new NumberInput("history-skip", 0, Infinity, /^\d+$/g)
        let skip = skipInput.GetValue()

        if (skip === null)
            return

        ShowHistory("/history", {actions: [...artistActions, ...trackActions, ...artistsGroupActions], limit: limit, skip: skip})
    })

    return info
}
