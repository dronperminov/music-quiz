function GetSearchParams() {
    return {
        query: document.getElementById("query").value.trim(),
        order: document.getElementById("order").value,
        order_type: +document.getElementById("order-type").value
    }
}

function LoadNotes(response, block) {
    for (let note of response.notes) {
        let artistId = `${note.artist_id}`
        let artist = new Artist(response.artist_id2artist[artistId])
        note = new Note(note)

        block.appendChild(note.Build(artist, response))
        block.appendChild(note.BuildTracks(artist, response))
        infos.Add(artist.BuildInfo())
    }

    return response.notes.length
}

function PushUrlParams(params = null) {
    let url = new URL(window.location.href)

    ClearSearchParams(url)

    if (params !== null) {
        if (params.query !== "")
            url.searchParams.set("query", params.query)

        url.searchParams.set("order", params.order)
        url.searchParams.set("order_type", params.order_type)
    }

    window.history.pushState(null, '', url.toString())
}

function SearchNotes() {
    let params = GetSearchParams()
    if (params === null)
        return

    PushUrlParams(params)

    search.CloseFiltersPopup()
    infiniteScroll.Reset()
    infiniteScroll.LoadContent()
}

function ClearNotes() {
    infiniteScroll.Reset()
    PushUrlParams()
    infiniteScroll.LoadContent()
}
