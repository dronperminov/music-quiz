function LoadTrack(trackId) {
    let audio = document.getElementById(`audio-${trackId}`)
    let error = document.getElementById(`error-${trackId}`)

    error.innerText = ""

    if (audio.hasAttribute("data-src")) {
        return new Promise((resolve, reject) => {
            audio.src = audio.getAttribute("data-src")
            resolve(true)
        })
    }

    return SendRequest("/get-direct-link", {yandex_id: audio.getAttribute("data-yandex-id")}).then(response => {
        if (response.status != "success") {
            error.innerText = response.message
            return false
        }

        audio.src = response.direct_link
        return true
    })
}

function PlayTrack(trackId) {
    let audio = document.getElementById(`audio-${trackId}`)
    audio.addEventListener("loadedmetadata", () => players.Add(trackId, audio, true))
    audio.addEventListener("play", () => players.Pause(audio))

    LoadTrack(trackId)
}
