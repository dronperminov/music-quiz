function ErrorSessionId(message) {
    let input = document.getElementById("session-id")
    input.classList.add("error-input")
    input.focus()

    ShowNotification(message, "error-notification", 3500)
}

function InputSessionId() {
    let input = document.getElementById("session-id")
    input.classList.remove("error-input")
}

function GetSessionId() {
    let input = document.getElementById("session-id")
    let sessionId = input.value.trim()
    input.value = sessionId

    if (sessionId === "") {
        ErrorSessionId("Идентификатор сессии не может быть пустым")
        return null
    }

    if (sessionId.match(/^[a-z\d]+$/gi) === null) {
        ErrorSessionId("Идентификатор сессии должен состоять только из латинских символов и цифр")
        return null
    }

    return sessionId
}

// TODO: disabled/enable buttons and input

function CreateSession() {
    let sessionId = GetSessionId()
    if (sessionId === null)
        return

    SendRequest("/create-multiplayer-session", {session_id: sessionId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось создать сессию с идентификатором "${sessionId}"<br><b>Причина</b>: ${response.message}`)
            localStorage.removeItem("sessionId")
            return
        }

        multiPlayer.Connect(sessionId, response.username)
    })
}

function ConnectSession() {
    let sessionId = GetSessionId()
    if (sessionId === null)
        return

    SendRequest("/check-multiplayer-session", {session_id: sessionId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось подключиться к сессии с идентификатором "${sessionId}"<br><b>Причина</b>: ${response.message}`)
            localStorage.removeItem("sessionId")
            return
        }

        multiPlayer.Connect(sessionId, response.username)
    })
}

function Load() {
    let sessionId = localStorage.getItem("sessionId")
    if (sessionId === null)
        return

    let input = document.getElementById("session-id")
    input.value = sessionId
    ConnectSession()
}

function Start() {
    SendRequest("/get-multi-player-question", {session_id: multiPlayer.sessionId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось получить вопрос<br><b>Причина</b>: ${response.message}`)
            return
        }
    })
}

function SendMultiplayerAnswer(correct, answerTime) {
    let answer = {
        correct: correct,
        session_id: multiPlayer.sessionId,
        username: multiPlayer.username,
        answer_time: answerTime
    }

    let buttons = [
        document.getElementById("answer-button-correct"),
        document.getElementById("answer-button-incorrect")
    ]

    for (let button of buttons)
        button.setAttribute("disabled", "")

    SendRequest("/answer-multi-player-question", answer).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(response.message, "error-notification")

            for (let button of buttons)
                button.removeAttribute("disabled")
        }
    })
}
