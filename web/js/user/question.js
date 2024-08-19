function ReplaceTrackData() {
    let image = document.getElementById("track-image")
    image.setAttribute("src", track.image_url)

    let title = document.getElementById("track-title")
    title.innerText = track.title

    let year = document.getElementById("track-year")
    year.innerText = track.year

    for (let artist of artists) {
        let link = document.getElementById(`link-artist-${artist.artist_id}`)
        link.setAttribute("href", `/artists/${artist.artist_id}`)
        link.innerText = artist.name
    }

    SetMediaSessionMetadata(track.track_id)
}

function ShowAnswer() {
    let menu = document.getElementById("track-menu")
    menu.removeAttribute("disabled")

    ReplaceTrackData()

    let showAnswerButton = document.getElementById("show-answer")
    showAnswerButton.classList.add("hidden")

    let answerBlock = document.getElementById("answer")
    answerBlock.classList.remove("hidden")

    let player = players.GetPlayer()
    player.SetTimecode("")
}

function SendAnswer(correct) {
    // TODO
    location.reload()
}
