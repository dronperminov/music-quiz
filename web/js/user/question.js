function InitQuestion() {
    if (answerTime !== null)
        return

    let showAnswerButton = document.getElementById("show-answer")
    showAnswerButton.classList.remove("hidden")

    answerTime = performance.now()
}

function ReplaceTrackData() {
    let image = document.getElementById("track-image")
    image.setAttribute("src", track.imageUrl)

    let circle = document.getElementById("track-circle")
    if (circle !== null)
        circle.classList.remove("hidden")

    let title = document.getElementById("track-title")
    title.innerText = track.title

    let year = document.getElementById("track-year")
    year.innerText = track.year

    let artistNames = []
    for (let artist of artists) {
        let link = document.getElementById(`link-artist-${artist.artist_id}`)
        link.setAttribute("href", `/artists/${artist.artist_id}`)
        link.innerText = artist.name
        artistNames.push(artist.name)
    }

    let query = `${artistNames.join(" ")} ${track.title} год выхода`
    year.href = `https://www.google.com/search?q=${encodeURIComponent(query)}`

    SetMediaSessionMetadata(track.trackId)
}

function ShowAnswer(correct = null) {
    if (answerTime !== null) {
        answerTime = (performance.now() - answerTime) / 1000
        let answerTimeSpan = document.getElementById("answer-time")
        answerTimeSpan.innerText = FormatTime(answerTime)
        answerTimeSpan.parentNode.classList.remove("hidden")
    }

    let menu = document.getElementById("track-menu")
    menu.removeAttribute("disabled")

    ReplaceTrackData()

    let trackModifications = document.getElementById("track-modifications")
    if (trackModifications !== null)
        trackModifications.classList.add("hidden")

    let showAnswerButton = document.getElementById("show-answer")
    showAnswerButton.classList.add("hidden")

    let answerBlock = document.getElementById("answer")
    answerBlock.classList.remove("hidden")

    let player = players.GetPlayer()

    if (player === null)
        return

    player.SetTimecode("")
    player.SetPlaybackRate(1)
    player.ShowIcons()

    if (correct === null)
        return

    let button = document.getElementById(`answer-button-${correct ? "incorrect" : "correct"}`)
    button.classList.add("hidden")
}

function SendAnswer(correct) {
    let answer = {correct: correct, group_id: groupId}

    if (answerTime !== null)
        answer.answer_time = answerTime

    let buttons = [
        document.getElementById("answer-button-correct"),
        document.getElementById("answer-button-incorrect")
    ]

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/answer-question", answer).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(response.message, "error-notification")

            for (let button of buttons)
                button.removeAttribute("disabled")

            return
        }

        location.reload()
    })
}
