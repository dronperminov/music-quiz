function GetParseInfo(response) {
    let parseInfo = [
        `<li><b>исполнители</b>: ${response.artists} (новые: ${response.new_artists})</li>`,
        `<li><b>треки</b>: ${response.tracks} (новые: ${response.new_tracks})</li>`
    ].join("")

    return `<ul>${parseInfo}</ul>`
}

function ParseArtists(buttons, artistIds, maxTracks = 20, maxArtists = 4, fromPlaylist = true) {
    if (artistIds.length == 0)
        return

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/parse-artists", {artist_ids: artistIds, max_tracks: maxTracks, max_artists: maxArtists, from_playlist: fromPlaylist}).then(response => {
        for (let button of buttons)
            button.removeAttribute("disabled")

        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось распарсить исполнител${artistIds.length == 1 ? "я" : "ей"}<br><b>Причина:</b> ${response.message}`, "error-notification")
            return
        }

        ShowNotification(`Исполнител${artistIds.length == 1 ? "ь успешно распаршен" : "и успешно распаршены"}.${GetParseInfo(response)}`, "success-notification")
    })
}

function ParseTracks(buttons, trackIds) {
    if (trackIds.length == 0)
        return

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/parse-tracks", {track_ids: trackIds}).then(response => {
        for (let button of buttons)
            button.removeAttribute("disabled")

        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось распарсить трек${trackIds.length == 1 ? "" : "и"}<br><b>Причина:</b> ${response.message}`, "error-notification")
            return
        }

        ShowNotification(`Трек${trackIds.length == 1 ? "успешно распаршен" : "и успешно распаршены"}.${GetParseInfo(response)}`, "success-notification")
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
            ShowNotification(`Чарт успешно обновлён.${GetParseInfo(response)}`, "success-notification")
    })
}

function AddArtist(buttons) {
    let urlRegex = /^https:\/\/music\.yandex\.ru\/artist\/(?<artistId>\d+)/g
    let urlInput = new TextInput("artist-url", urlRegex, "Введена некорректная ссылка", true)
    let urls = urlInput.GetValue()
    if (urls === null)
        return

    let maxTracksInput = new NumberInput("artist-max-tracks", 1, 100, /^\d+$/g)
    let maxTracks = maxTracksInput.GetValue()
    if (maxTracks === null)
        return

    let maxArtistsInput = new NumberInput("artist-max-artists", 1, 5, /^\d+$/g)
    let maxArtists = maxArtistsInput.GetValue()
    if (maxArtists === null)
        return

    let fromPlaylist = document.getElementById("artist-from-playlist").checked

    let artistIds = Array.from(new Set(urls.map(url => /artist\/(?<artistId>\d+)/g.exec(url).groups.artistId)))
    ParseArtists(buttons, artistIds, maxTracks, maxArtists, fromPlaylist)
}

function AddTrack(buttons) {
    let urlRegex = /^https:\/\/music\.yandex\.ru\/(album\/\d+\/)?track\/(?<trackId>\d+)/g
    let urlInput = new TextInput("track-url", urlRegex, "Введена некорректная ссылка", true)
    let urls = urlInput.GetValue()
    if (urls === null)
        return

    let trackIds = Array.from(new Set(urls.map(url => /track\/(?<trackId>\d+)/g.exec(url).groups.trackId)))
    ParseTracks(buttons, trackIds)
}
