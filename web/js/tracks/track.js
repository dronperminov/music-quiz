function LoadTrack(trackId) {
    let audio = document.getElementById(`audio-${trackId}`)
    let loader = document.getElementById(`loader-${trackId}`)
    let loadIcon = document.getElementById(`player-${trackId}-load`)
    let error = document.getElementById(`error-${trackId}`)

    error.innerText = ""

    if (audio.hasAttribute("data-src")) {
        return new Promise((resolve, reject) => {
            audio.src = audio.getAttribute("data-src")
            resolve(true)
        })
    }

    return SendRequest("/get-direct-link", {yandex_id: audio.getAttribute("data-yandex-id")}).then(response => {
        loader.classList.add("hidden")

        if (response.status != "success") {
            error.innerText = response.message
            audio.classList.remove("loaded")
            loadIcon.classList.remove("hidden")
            return false
        }

        audio.src = response.direct_link
        return true
    })
}

function PlayTrack(trackId) {
    let audio = document.getElementById(`audio-${trackId}`)
    let loader = document.getElementById(`loader-${trackId}`)
    let loadIcon = document.getElementById(`player-${trackId}-load`)

    if (audio.classList.contains("loaded"))
        return

    audio.classList.add("loaded")
    loader.classList.remove("hidden")
    loadIcon.classList.add("hidden")

    audio.addEventListener("loadedmetadata", () => players.Add(trackId, audio, true))
    audio.addEventListener("play", () => players.Pause(audio))

    LoadTrack(trackId)
}
