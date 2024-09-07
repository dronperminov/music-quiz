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

    let removeStatistics = document.getElementById("remove-statistics-on-connect").checked

    SendRequest("/check-multiplayer-session", {session_id: sessionId, remove_statistics: removeStatistics}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось подключиться к сессии с идентификатором "${sessionId}"<br><b>Причина</b>: ${response.message}`)
            localStorage.removeItem("sessionId")
            return
        }

        multiPlayer.Connect(sessionId, response.username)
    })
}

function RemoveSession() {
    if (multiPlayer.sessionId === null)
        return

    if (!confirm("Вы уверены, что хотите удалить сессию?"))
        return

    SendRequest("/remove-multiplayer-session", {session_id: multiPlayer.sessionId}).then(response => {
        if (response.status != SUCCESS_STATUS) {
            ShowNotification(`Не удалось удалить сессию с идентификатором "${multiPlayer.sessionId}"<br><b>Причина</b>: ${response.message}`)
            localStorage.removeItem("sessionId")
            return
        }

        multiPlayer.Disconnect()
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
