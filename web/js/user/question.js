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

    let miraclesField = document.getElementById("miracles-field")
    if (miraclesField !== null)
        for (let div of miraclesField.getElementsByTagName("span"))
            div.classList.remove("hidden")

    let showAnswerButton = document.getElementById("show-answer")
    showAnswerButton.classList.add("hidden")

    let answerBlock = document.getElementById("answer")
    answerBlock.classList.remove("hidden")

    ResetPlayer()

    if (correct === null)
        return

    let button = document.getElementById(`answer-button-${correct ? "incorrect" : "correct"}`)
    button.classList.add("hidden")
}

function ResetPlayer() {
    let player = players.GetPlayer()

    if (player !== null) {
        player.Reset()

        if (player.audio.hasAttribute("data-answer-seek"))
            player.Seek(+player.audio.getAttribute("data-answer-seek"))
        return
    }

    setTimeout(() => ResetPlayer(), 1000)
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
