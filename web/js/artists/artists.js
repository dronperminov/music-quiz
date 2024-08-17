function GetSearchParams() {
    let listenCount = listenCountInput.GetValue()

    if (listenCount === null)
        return null

    return {
        query: document.getElementById("query").value,
        order: document.getElementById("order").value,
        order_type: +document.getElementById("order-type").value,
        listen_count: listenCount,
        genres: genresInput.GetValue(),
        artist_type: artistTypeInput.GetValue(),
        artists_count: artistsCountInput.GetValue(),
        language: languageInput.GetValue()
    }
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
    let error = document.getElementById("error")

    status = "loading"
    loader.classList.remove("hidden")
    results.innerText = ""
    error.innerText = ""

    let searchParams = GetSearchParams()

    if (searchParams === null)
        return

    search.CloseFiltersPopup()

    SendRequest("/artists", {...searchParams, page: page, page_size: pageSize}).then(response => {
        status = "loaded"

        if (response.status != SUCCESS_STATUS) {
            error.innerText = response.message
            status = "error"
            setTimeout(() => {
                status = "";
                LoadArtists(pageSize)
            }, 2000)
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
            artists.appendChild(artist.Build())
            infoBlock.appendChild(artist.BuildInfo())
        }

        infos.Update()
    })
}

function ClearSearchArtists() {
    for (let shortArtists of document.getElementsByClassName("short-artists-block"))
        shortArtists.classList.remove("hidden")

    let artists = document.getElementById("artists")
    let infoBlock = document.getElementById("info-block")
    let results = document.getElementById("search-results")

    artists.innerHTML = ""
    infoBlock.innerHTML = ""
    results.innerText = ""
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

function SearchShortArtists(order, orderType) {
    let queryInput = document.getElementById("query")
    let orderInput = document.getElementById("order")
    let orderTypeInput = document.getElementById("order-type")

    page = 0
    status = ""

    queryInput.value = ""
    orderInput.value = order
    orderTypeInput.value = orderType
    listenCountInput.Clear()
    genresInput.Clear()
    artistTypeInput.Clear()

    SearchArtists()
}
