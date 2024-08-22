function ParseArtist(buttons, artistId, maxTracks = 20, maxArtists = 4) {
    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/parse-artist", {artist_id: artistId, max_tracks: maxTracks, max_artists: maxArtists}).then(response => {
        for (let button of buttons)
            button.removeAttribute("disabled")

        if (response.status != SUCCESS_STATUS)
            ShowNotification(`Не удалось распарсить исполнителя<br><b>Причина:</b> ${response.message}`, "error-notification")
        else
            ShowNotification(`Исполнитель успешно распаршен.<ul><li>треки: ${response.tracks}</li><li>исполнители: ${response.artists}</li></ul>`, "success-notification")
    })
}

function ParseChart(buttons) {
    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/parse-chart", {}).then(response => {
        for (let button of buttons)
            button.removeAttribute("disabled")

        if (response.status != SUCCESS_STATUS)
            ShowNotification(`Не удалось распарсить чарт<br><b>Причина:</b> ${response.message}`, "error-notification")
        else
            ShowNotification(`Чарт успшено обновлён.<ul><li>треки: ${response.tracks}</li><li>исполнители: ${response.artists}</li></ul>`, "success-notification")
    })
}

function AddArtist(buttons) {
    let urlRegex = /^https:\/\/music\.yandex\.ru\/artist\/(?<artistId>\d+)/g
    let urlInput = new TextInput("artist-url", urlRegex, "Введена некорректная ссылка")
    let url = urlInput.GetValue()
    if (url === null)
        return

    let maxTracksInput = new NumberInput("artist-max-tracks", 1, 20, /^\d+$/g)
    let maxTracks = maxTracksInput.GetValue()
    if (maxTracks === null)
        return

    let maxArtistsInput = new NumberInput("artist-max-artists", 1, 5, /^\d+$/g)
    let maxArtists = maxArtistsInput.GetValue()
    if (maxArtists === null)
        return

    let artistId = urlRegex.exec(url).groups.artistId
    ParseArtist(buttons, artistId, maxTracks, maxArtists)
}
