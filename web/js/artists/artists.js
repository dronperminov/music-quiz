function GetSearchParams() {
    let order = document.getElementById("order").value
    let orderType = +document.getElementById("order-type").value
    return {order: order, order_type: orderType}
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

    loading = true
    loader.classList.remove("hidden")
    error.innerText = ""

    let searchParams = GetSearchParams()

    SendRequest("/artists", {...searchParams, page: page, page_size: pageSize}).then(response => {
        loader.classList.add("hidden")
        loading = false

        if (response.status != SUCCESS_STATUS) {
            error.innerText = response.error
            return
        }

        page += 1

        for (let artist of response.artists) {
            artist = new Artist(artist)
            artists.appendChild(artist.Build())
            infoBlock.appendChild(artist.BuildInfo())
        }

        infos.Update()
    })
}

function ScrollArtists() {
    if (page == 0 || loading)
        return

    let artists = document.getElementById("artists")
    let end = artists.offsetTop + artists.clientHeight
    let scroll = window.innerHeight + window.scrollY
    
    if (scroll >= end - 100)
        LoadArtists()
}
