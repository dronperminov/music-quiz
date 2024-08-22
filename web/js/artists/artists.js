function GetSearchParams() {
    let listenCount = listenCountInput.GetValue()

    if (listenCount === null)
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
        tracks_count: tracksCount,
        added_tracks: addedTracks,
        genres: genresInput.GetValue(),
        artist_type: artistTypeInput.GetValue(),
        artists_count: artistsCountInput.GetValue(),
        language: languageInput.GetValue()
    }
}

function PushUrlParams(params) {
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

        for (let key of ["listen_count", "tracks_count", "added_tracks"])
            if (params[key][0] !== "" || params[key][1] !== "")
                url.searchParams.set(key, JSON.stringify(params[key]))

        for (let key of ["genres", "artist_type", "artists_count", "language"])
            if (Object.keys(params[key]).length > 0)
                url.searchParams.set(key, JSON.stringify(params[key]))
    }

    window.history.pushState(null, '', url.toString())
}

function SearchArtists() {
    for (let shortArtists of document.getElementsByClassName("short-artists-block"))
        shortArtists.classList.add("hidden")

    let results = document.getElementById("search-results")
    let artists = document.getElementById("artists")
    let infoBlock = document.getElementById("info-block")

    results.innerText = ""
    artists.innerHTML = ""
    infoBlock.innerHTML = ""
    page = 0

    LoadArtists()
}

function LoadArtists(pageSize = 10) {
    let results = document.getElementById("search-results")
    let artists = document.getElementById("artists")
    let infoBlock = document.getElementById("info-block")

    let loader = document.getElementById("loader")

    status = "loading"
    loader.classList.remove("hidden")
    results.innerText = ""

    let searchParams = GetSearchParams()

    if (searchParams === null)
        return

    search.CloseFiltersPopup()

    if (page == 0)
        PushUrlParams(searchParams)

    SendRequest("/artists", {...searchParams, page: page, page_size: pageSize}).then(response => {
        status = "loaded"

        if (response.status != SUCCESS_STATUS) {
            ShowNotification(response.message, "error-notification", 1500)
            status = "error"
            setTimeout(RetrySearch, 3500)
            return
        }

        loader.classList.add("hidden")

        if (response.total > 0)
            results.innerText = `${GetWordForm(response.total, ['исполнитель нашёлся', 'исполнителя нашлось', 'исполнителей нашлось'])} по запросу`
        else
            results.innerText = "К сожалению, по запросу ничего не нашлось"

        if (response.artists.length < pageSize)
            status = "loading"

        page += 1

        for (let artist of response.artists) {
            artist = new Artist(artist)
            artists.appendChild(artist.Build(response.artist_id2scale))
            infos.Add(artist.BuildInfo())
        }
    })
}

function RetrySearch(pageSize) {
    if (status == "error") {
        status = "";
        LoadArtists(pageSize)
    }
    else {
        loader.classList.add("hidden")
    }
}

function ClearSearchArtists() {
    for (let shortArtists of document.getElementsByClassName("short-artists-block"))
        shortArtists.classList.remove("hidden")

    let artists = document.getElementById("artists")
    let infoBlock = document.getElementById("info-block")
    let results = document.getElementById("search-results")

    let loader = document.getElementById("loader")

    artists.innerHTML = ""
    infoBlock.innerHTML = ""
    results.innerText = ""
    loader.classList.add("hidden")
    status = ""
    page = 0

    PushUrlParams(null)
}

function ScrollArtists() {
    if (page == 0 || status == "loading" || status == "error")
        return

    let artists = document.getElementById("artists")
    let end = artists.offsetTop + artists.clientHeight
    let scroll = window.innerHeight + window.scrollY
    
    if (scroll >= end - 100)
        LoadArtists()
}

function SearchShortArtists(order, orderType, target = "all") {
    let queryInput = document.getElementById("query")
    let targetInput = document.getElementById("target")
    let orderInput = document.getElementById("order")
    let orderTypeInput = document.getElementById("order-type")

    page = 0
    status = ""

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

    let urlBlock = MakeElement("info-input-line", info)
    let urlLabel = MakeElement("", urlBlock, {innerText: "Ссылка:", "for": "artist-url"}, "label")
    let urlInput = MakeElement("basic-input", urlBlock, {type: "text", value: "", placeholder: "https://music.yandex.ru/artist/...", id: "artist-url"}, "input")
    MakeElement("error", info, {id: "artist-url-error"})

    let maxTracksBlock = MakeElement("info-input-line", info)
    let maxTracksLabel = MakeElement("", maxTracksBlock, {innerText: "Треков не более:", "for": "artist-max-tracks"}, "label")
    let maxTracksInput = MakeElement("basic-input", maxTracksBlock, {type: "text", value: "20", id: "artist-max-tracks"}, "input")
    MakeElement("error", info, {id: "artist-max-tracks-error"})

    let maxArtistsBlock = MakeElement("info-input-line", info)
    let maxArtistsLabel = MakeElement("", maxArtistsBlock, {innerText: "Исполнителей трека не более:", "for": "artist-max-artists"}, "label")
    let maxArtistsInput = MakeElement("basic-input", maxArtistsBlock, {type: "text", value: "4", id: "artist-max-artists"}, "input")
    MakeElement("error", info, {id: "artist-max-artists-error"})

    let artistButton = MakeElement("basic-button gradient-button", info, {innerText: "Добавить"}, "button")

    urlLabel.addEventListener("click", () => {
        urlInput.value = ""
        urlInput.focus()
    })

    chartButton.addEventListener("click", () => ParseChart([chartButton, artistButton]))
    artistButton.addEventListener("click", () => AddArtist([chartButton, artistButton]))

    return info
}
