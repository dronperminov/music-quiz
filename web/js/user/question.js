function InitQuestion() {
    if (answerTime !== null)
        return

    let showAnswerButton = document.getElementById("show-answer")
    showAnswerButton.classList.remove("hidden")

    answerTime = performance.now()
}

function ShowAnswer(correct = null) {
    if (answerTime !== null) {
        answerTime = (performance.now() - answerTime) / 1000
        let answerTimeSpan = document.getElementById("answer-time")
        answerTimeSpan.innerText = FormatTime(answerTime)
        answerTimeSpan.parentNode.classList.remove("hidden")
    }

    track.ReplaceUnknown(artists)

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
    let answer = questionId === null ? {correct: correct, group_id: groupId} : {correct: correct, question_id: questionId}
    let url = questionId === null ? "/answer-question" : "/answer-quiz-tour-question"

    if (answerTime !== null)
        answer.answer_time = answerTime

    let buttons = [
        document.getElementById("answer-button-correct"),
        document.getElementById("answer-button-incorrect")
    ]

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest(url, answer).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(response.message, "error-notification")

            for (let button of buttons)
                button.removeAttribute("disabled")

            return
        }

        location.reload()
    })
}
