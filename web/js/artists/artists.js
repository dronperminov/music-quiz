function GetSearchParams() {
    let query = document.getElementById("query").value
    let order = document.getElementById("order").value
    let orderType = +document.getElementById("order-type").value

    return {
        query: query,
        order: order,
        order_type: orderType
    }
}

function SearchArtists() {
    for (let shortArtists of document.getElementsByClassName("short-artists-block"))
        shortArtists.classList.add("hidden")

    let artists = document.getElementById("artists")
    let infoBlock = document.getElementById("info-block")

    artists.innerHTML = ""
    infoBlock.innerHTML = ""
    page = 0

    LoadArtists()
}

function LoadArtists(pageSize = 10) {
    let artists = document.getElementById("artists")
    let infoBlock = document.getElementById("info-block")

    let loader = document.getElementById("loader")
    let error = document.getElementById("error")
    let noResults = document.getElementById("no-results")

    status = "loading"
    loader.classList.remove("hidden")
    noResults.classList.add("hidden")
    error.innerText = ""

    let searchParams = GetSearchParams()

    SendRequest("/artists", {...searchParams, page: page, page_size: pageSize}).then(response => {
        loader.classList.add("hidden")
        status = "loaded"

        if (response.status != SUCCESS_STATUS) {
            error.innerText = response.error
            status = ""
            return
        }

        if (page == 0 && response.artists.length == 0)
            noResults.classList.remove("hidden")

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
    let noResults = document.getElementById("no-results")

    artists.innerHTML = ""
    infoBlock.innerHTML = ""
    noResults.classList.add("hidden")
}

function ScrollArtists() {
    if (page == 0 || status == "loading")
        return

    let artists = document.getElementById("artists")
    let end = artists.offsetTop + artists.clientHeight
    let scroll = window.innerHeight + window.scrollY
    
    if (scroll >= end - 100)
        LoadArtists()
}
